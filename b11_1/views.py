from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Material, Zuteilung, Auspraegung, G_Partner
from .forms_il import MaterialForm_IL
from .forms_gd import MaterialForm_GD
from .forms_smda import MaterialForm_SMDA
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .mixins import grIL_GroupRequiredMixin, grGD_GroupRequiredMixin, grSMDA_GroupRequiredMixin
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db import connections
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import IntegerField
from .export_utils import export_to_excel
from django.contrib import messages
import re
from .mixins import FormValidMixin
from django.template import RequestContext


def custom_permission_denied_view(request, exception=None):
    response = render(request, '403.html')
    response.status_code = 403
    return response

def home(request):
   return redirect('list-material')

class CustomLoginView(LoginView):
    template_name = 'login_user.html'
    def form_invalid(self, form):
        messages.error(self.request, "Benutzername und/oder Passwort ungültig.")
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.groups.filter(name='grIL').exists():
            return redirect('list-material-il')
        elif self.request.user.groups.filter(name='grGD').exists():
            return redirect('list-material-gd')
        elif self.request.user.groups.filter(name='grSMDA').exists():
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_material_il_transferred = Material.objects.filter(is_transferred=True, hersteller=self.request.user, is_archived=False)
        list_material_il = Material.objects.filter(is_transferred=False, hersteller=self.request.user, is_archived=False)

        # Convert positions_nr to integers for sorting
        context['list_material_il_transferred'] = sorted(list_material_il_transferred, key=lambda x: int(x.positions_nr))
        context['list_material_il'] = sorted(list_material_il, key=lambda x: int(x.positions_nr))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=True, transfer_date=timezone.now())
            elif action == 'delete':
                selected_materials.delete()
            elif action == 'archive':
                selected_materials.update(is_archived=True)

        return redirect(reverse('list-material-il'))

class AddMaterial_IL_View(FormValidMixin, grIL_GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'il/add_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list-material-il')
    success_message = "Das Material wurde erfolgreich hinzugefügt."

class UpdateMaterial_IL_View(FormValidMixin, grIL_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'il/update_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list-material-il')
    success_message = "Das Material wurde erfolgreich aktualisiert."

class ShowMaterial_IL_View(grIL_GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'il/show_material_il.html'
    form_class = MaterialForm_IL

class ListMaterial_GD_View(grGD_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'gd/list_material_gd.html'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=False)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_material_archived_gd = Material.objects.filter(is_transferred=True, is_archived=True)
        list_material_gd = Material.objects.filter(is_transferred=True, is_archived=False)

        # Convert positions_nr to integers for sorting
        context['list_material_archived_gd'] = sorted(list_material_archived_gd, key=lambda x: int(x.positions_nr))
        context['list_material_gd'] = sorted(list_material_gd, key=lambda x: int(x.positions_nr))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=False, transfer_date=timezone.now())
            elif action == 'archive':
                selected_materials.update(is_archived=True)
            elif action == 'delete':
                selected_materials.delete()
            elif action == 'export':
                return export_to_excel(selected_materials)

        return redirect(reverse('list-material-gd'))

class ListMaterialArchived_GD_View(grGD_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'gd/list_material_archived_gd.html'
    context_object_name = 'list_material_archived_gd'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

class UpdateMaterial_GD_View(grGD_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'gd/update_material_gd.html'
    form_class = MaterialForm_GD
    success_url = reverse_lazy('list-material-gd')
    success_message = "Das Material wurde erfolgreich aktualisiert."

    def form_valid(self, form):
        item = form.save(commit=False)
        if item.chargenpflicht == True:
            item.materialzustandsverwaltung = "1"
        elif item.chargenpflicht == False:
            item.materialzustandsverwaltung = "2"
        print("item.materialzustandsverwaltung = " + item.materialzustandsverwaltung)
        item.save()
        return super().form_valid(form)

class ShowMaterial_GD_View(grGD_GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'gd/show_material_gd.html'
    form_class = MaterialForm_GD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context    

class ListMaterial_SMDA_View(grSMDA_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'smda/list_material_smda.html'
    context_object_name = 'list_material_smda'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=False)
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

        return redirect(reverse('list-material-smda'))

class ListMaterialArchived_SMDA_View(grSMDA_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'smda/list_material_archived_smda.html'
    context_object_name = 'list_material_archived_smda'

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

class UpdateMaterial_SMDA_View(grSMDA_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'smda/update_material_smda.html'
    form_class = MaterialForm_SMDA
    success_url = reverse_lazy('list-material-smda')
    success_message = "Das Material wurde erfolgreich aktualisiert."

    def form_valid(self, form):
        item = form.save(commit=False)
        if item.werk_1 == "0800":
            item.verkaufsorg = "A100"
        else:
            item.verkaufsorg = "M100"
        print("item.verkaufsorg = " + item.verkaufsorg)
        print("item.zuteilung_id = " + str(item.zuteilung_id))
        zuteilung = Zuteilung.objects.filter(id=item.zuteilung_id).first()
        auspraegung = Auspraegung.objects.filter(id=item.auspraegung_id).first()
        print("item.zuteilung = " + str(zuteilung.text))
        if zuteilung.text == "MKZ" and auspraegung.text == "04":
            form.add_error('auspraegung', "Die Ausprägung mit 'MKZ' muss '01', '02' oder '03' sein.")
        if zuteilung.text == "PRD" and auspraegung.text == "04":
            form.add_error('auspraegung', "Die Ausprägung mit 'PRD' muss '01', '02' oder '03' sein.")

        if form.errors:
            return self.form_invalid(form)

        item.save()
        return super().form_valid(form)

class ShowMaterial_SMDA_View(grSMDA_GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'smda/show_material_smda.html'
    form_class = MaterialForm_SMDA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context    

