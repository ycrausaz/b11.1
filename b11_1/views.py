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

# Create your views here.

def home(request):
   return redirect('list-material')

def export_to_excel(materials):
    # Define your database views and their specific columns
    views = {
        'view1': ['col1', 'col2', 'col3'],
        'view2': ['colA', 'colB', 'colC'],
        # Add all your view names and their specific columns here
    }

    # Define the column header tokens for each view
    header_tokens = {
        'view1': {
            'col1': 'Token1',
            'col2': 'Token2',
            'col3': 'Token3',
        },
        'view2': {
            'colA': 'TokenA',
            'colB': 'TokenB',
            'colC': 'TokenC',
        },
        # Add header tokens for all your views here
    }

    # Open a connection to the database
    connection = connections['default']

    # Create a Pandas Excel writer using openpyxl as the engine
    with pd.ExcelWriter('database_views.xlsx', engine='openpyxl') as writer:
        for view, columns in views.items():
            # Execute a raw SQL query to fetch all data from the view
            query = f'SELECT {", ".join(columns)} FROM {view}'
            df = pd.read_sql_query(query, connection)

            # Rename the DataFrame columns using the header tokens
            df.columns = [header_tokens[view].get(col, col) for col in df.columns]

            # Write the DataFrame to a specific sheet
            df.to_excel(writer, sheet_name=view, index=False)

        # Also write the selected materials to a new sheet
        selected_df = pd.DataFrame(list(materials.values()))
        # Assuming 'materials' has consistent column names across views
        selected_df.columns = [col.capitalize().replace('_', ' ') for col in selected_df.columns]
        selected_df.to_excel(writer, sheet_name='Selected Materials', index=False)

    # Create the HttpResponse object with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=database_views.xlsx'

    # Write the Excel file to the response
    writer.save()
    response.write(open('database_views.xlsx', 'rb').read())

    return response

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
       qs = super().get_queryset(**kwargs)
       return qs.filter(is_transferred=False).order_by('positions_nr')

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=True, transfer_date=timezone.now())
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
       qs = super().get_queryset(**kwargs)
       return qs.filter(is_transferred=True).order_by('positions_nr')

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
       qs = super().get_queryset(**kwargs)
       return qs.filter(is_transferred=True).order_by('positions_nr')

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
