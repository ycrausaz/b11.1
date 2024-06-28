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

# Create your views here.

def home(request):
   return redirect('list-material')

#class UserLogin(View):
#    def post(self, request, *args, **kwargs):
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return redirect('list-material')
#        else:
##            messages.success(request, ("Erreur dans le login"))
#            return redirect('login-user')

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
       qs = super().get_queryset(**kwargs)
       return qs.filter(is_transferred=True).order_by('positions_nr')

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

class ExportView(View):
    def get(self, request):
        form = ExportForm()
        return render(request, 'export.html', {'form': form})

    def post(self, request):
        form = ExportForm(request.POST)
        if form.is_valid():
            # Define your database views and column header tokens
            views = {
                'view1': ['col1', 'col2', 'col3'],
                'view2': ['col1', 'col2', 'col3'],
                # Add all your view names and their columns here
            }

            header_tokens = {
                'col1': 'Token1',
                'col2': 'Token2',
                'col3': 'Token3',
                # Map all your column names to tokens here
            }

            # Open a connection to the database
            connection = connections['default']

            # Create a Pandas Excel writer using openpyxl as the engine
            with pd.ExcelWriter('database_views.xlsx', engine='openpyxl') as writer:
                for view, columns in views.items():
                    query = f'SELECT {", ".join(columns)} FROM {view}'
                    df = pd.read_sql_query(query, connection)
                    df.columns = [header_tokens[col] for col in df.columns]
                    df.to_excel(writer, sheet_name=view, index=False)

            # Create the HttpResponse object with the appropriate Excel header
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=database_views.xlsx'

            # Write the Excel file to the response
            writer.save()
            response.write(open('database_views.xlsx', 'rb').read())

            return response

        return render(request, 'export.html', {'form': form})
