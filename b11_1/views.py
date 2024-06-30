from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Material
from .forms import MaterialForm_IL, MaterialForm_GD, MaterialForm_SMDA
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .mixins import grIL_GroupRequiredMixin, grGD_GroupRequiredMixin, grSMDA_GroupRequiredMixin
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db import connections
from .forms import ExportForm
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.utils.timezone import is_aware

# Create your views here.

def home(request):
   return redirect('list-material')

def export_to_excel(materials):
    export_to_excel_type_1(materials)

#        # Define your database views and their specific columns
#        views = {
#            'MKVE_Verkaufsdaten': ['col1', 'col2', 'col3', 'col4'],
#            'view2': ['colA', 'colB', 'colC'],
#            # Add all your view names and their specific columns here
#        }
#    
#        # Define the column header tokens for each view
#        header_tokens = {
#            'MKVE_Verkaufsdaten': {
#                'col1': 'SOURCE_ID',
#                'col2': 'VKORG',
#                'col3': 'VTWEG',
#                'col4': 'MTPOS',
#            },
#            'view2': {
#                'colA': 'TokenA',
#                'colB': 'TokenB',
#                'colC': 'TokenC',
#            },
#            # Add header tokens for all your views here
#        }

def make_timezone_naive(df):
    for col in df.select_dtypes(include=['datetime64[ns]']).columns:
        df[col] = df[col].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) and is_aware(x) else x)
    return df

def export_to_excel(materials):
#    try:
        # Define your database views and their specific columns
        views = {
            'MKVE_Verkaufsdaten': ['SOURCE_ID', 'VKORG', 'VTWEG', 'MTPOS'],
#            'view2': ['colA', 'colB', 'colC'],
            # Add all your view names and their specific columns here
        }
    
        # Define the column header tokens for each view
        header_tokens = {
            'MKVE_Verkaufsdaten': {
                'col1': 'SOURCE_ID',
                'col2': 'VKORG',
                'col3': 'VTWEG',
                'col4': 'MTPOS',
            },
 #           'view2': {
 #               'colA': 'TokenA',
 #               'colB': 'TokenB',
 #               'colC': 'TokenC',
 #           },
            # Add header tokens for all your views here
        }

        connection = connections['default']
        print("*** connection ok")

        with pd.ExcelWriter('database_views.xlsx', engine='openpyxl') as writer:
            sheet_added = False
            for view, columns in views.items():
                try:
                    query = f'SELECT {", ".join(columns)} FROM {view}'
                    df = pd.read_sql_query(query, connection)

                    df = make_timezone_naive(df)

                    df.columns = [header_tokens[view].get(col, col) for col in df.columns]

                    df.to_excel(writer, sheet_name=view, index=False)
                    sheet_added = True
                except Exception as e:
                    print(f"Error fetching data for view '{view}': {e}")

            if not sheet_added:
                # Add an empty sheet if no data was added
                pd.DataFrame().to_excel(writer, sheet_name='EmptySheet')

            selected_df = pd.DataFrame(list(materials.values()))
            if not selected_df.empty:
                selected_df = make_timezone_naive(selected_df)
                selected_df.columns = [col.capitalize().replace('_', ' ') for col in selected_df.columns]
                selected_df.to_excel(writer, sheet_name='Selected Materials', index=False)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=database_views.xlsx'

        with open('database_views.xlsx', 'rb') as file:
            response.write(file.read())

        return response
#    except Exception as e:
#        print(f"Error generating Excel file: {e}")
#        return HttpResponse("An error occurred while generating the Excel file.", status=500)

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.groups.filter(name='grIL').exists():
            print("grIL")
            return redirect('list-material-il')
        elif self.request.user.groups.filter(name='grGD').exists():
            print("grGS")
            return redirect('list-material-gd')
        elif self.request.user.groups.filter(name='grSMDA').exists():
            print("grSMDA")
            return redirect('list-material-smda')
        return response

    def get(self, request, *args, **kwargs):
        return render(request, 'login_user.html', {}) 

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login-user')

class ListMaterial_View(ListView):
    model = Material
    template_name = 'list_material.html'
    context_object_name = 'list_material'

class ListMaterial_IL_View(grIL_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'il/list_material_il.html'
    context_object_name = 'list_material_il'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=False)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
#                selected_materials.update(is_transferred=True, transfer_date=timezone.now())
                selected_materials.update(is_transferred=True)
            elif action == 'delete':
                selected_materials.delete()

        return redirect(reverse('list-material-il'))

class AddMaterial_IL_View(grIL_GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'il/add_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('add-material-il')
    success_message = "Le matériel a été ajouté avec succès."

class UpdateMaterial_IL_View(grIL_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'il/update_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list-material-il')
    success_message = "Le matériel a été ajouté avec succès."

class ShowMaterial_IL_View(grIL_GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'il/show_material_il.html'
    form_class = MaterialForm_IL

class ListMaterial_GD_View(grGD_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'gd/list_material_gd.html'
    context_object_name = 'list_material_gd'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=False, transfer_date=timezone.now())
            elif action == 'delete':
                selected_materials.delete()
            elif action == 'export':
                return export_to_excel(selected_materials)

        return redirect(reverse('list-material-gd'))

class AddMaterial_GD_View(grGD_GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'gd/add_material_gd.html'
    form_class = MaterialForm_GD
    success_url = reverse_lazy('add-material-gd')
    success_message = "Le matériel a été ajouté avec succès."

class UpdateMaterial_GD_View(grGD_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'gd/update_material_gd.html'
    form_class = MaterialForm_GD
    success_url = reverse_lazy('list-material-gd')
    success_message = "Le matériel a été ajouté avec succès."

class ShowMaterial_GD_View(grGD_GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'gd/show_material_gd.html'
    form_class = MaterialForm_GD

class ListMaterial_SMDA_View(grSMDA_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'smda/list_material_smda.html'
    context_object_name = 'list_material_smda'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=False, transfer_date=timezone.now())
            elif action == 'delete':
                selected_materials.delete()

        return redirect(reverse('list-material-smda'))

class AddMaterial_SMDA_View(grSMDA_GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'smda/add_material_smda.html'
    form_class = MaterialForm_SMDA
    success_url = reverse_lazy('add-material-smda')
    success_message = "Le matériel a été ajouté avec succès."

class UpdateMaterial_SMDA_View(grSMDA_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'smda/update_material_smda.html'
    form_class = MaterialForm_SMDA
    success_url = reverse_lazy('list-material-smda')
    success_message = "Le matériel a été ajouté avec succès."

class ShowMaterial_SMDA_View(grSMDA_GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'smda/show_material_smda.html'
    form_class = MaterialForm_SMDA
