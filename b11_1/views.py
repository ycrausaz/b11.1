from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Material, View_IL
from .forms import MaterialForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

# Create your views here.

def home(request):
   return redirect('list-material')

class UserLogin(View):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list-material')
        else:
#            messages.success(request, ("Erreur dans le login"))
            return redirect('login-user')

    def get(self, request, *args, **kwargs):
        return render(request, 'login_user.html', {}) 

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login-user')

class ListMaterial_IL_View(ListView):
    model = View_IL
    template_name = 'il/list_material_il.html'
    context_object_name = 'list_material_il'

class ListMaterial_View(ListView):
    model = Material
    template_name = 'list_material.html'
    context_object_name = 'list_material'

class AddMaterial_IL(SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'il/add_material_il.html'
    form_class = MaterialForm
    success_url = reverse_lazy('add-material-il')
    success_message = "Le client a été ajouté avec succès."
