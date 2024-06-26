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

