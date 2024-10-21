from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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
from .mixins import grIL_GroupRequiredMixin, grGD_GroupRequiredMixin, grSMDA_GroupRequiredMixin, grAdmin_GroupRequiredMixin
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db import connections
from django.db import connection
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import IntegerField
from .export_utils import export_to_excel
from django.contrib import messages
import re
from .mixins import FormValidMixin
from django.template import RequestContext
from .forms import CustomPasswordChangeForm
from .forms import CustomPasswordResetForm
from b11_1.models import Profile, Material
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def custom_permission_denied_view(request, exception=None):
    response = render(request, '403.html')
    response.status_code = 403
    return response

def home(request):
   return redirect('login_user')

class CustomLoginView(LoginView):
    template_name = 'login_user.html'
    
    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            profile = user.profile
            profile.failed_login_attempts += 1
            profile.save()

            if profile.failed_login_attempts >= 3:
                current_site = get_current_site(self.request)
                mail_subject = 'Reset your password'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})      
                reset_url = f'http://{current_site.domain}{reset_link}'
                message = f'It seems you have failed to login 3 times. Please reset your password using the following link:\n{reset_url}'
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                logger.info(f'Password reset email sent to user: {username}')
                logger.info(message)
                
                messages.warning(
                    self.request,
                    "You have entered an incorrect password 3 times. "
                    "A password reset link has been sent to your email."
                )
                
                profile.failed_login_attempts = 0
                profile.save()
            else:
                messages.error(self.request, "Benutzername und/oder Passwort ungültig.")
        except User.DoesNotExist:
            messages.error(self.request, "Benutzername und/oder Passwort ungültig.")
        
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        profile.failed_login_attempts = 0  # Reset failed attempts on successful login
        profile.save()
        if profile.is_first_login:
            return redirect('password_change')
        if self.request.user.groups.filter(name='grIL').exists():
            return redirect('list_material_il')
        elif self.request.user.groups.filter(name='grGD').exists():
            return redirect('list_material_gd')
        elif self.request.user.groups.filter(name='grSMDA').exists():
            return redirect('list_material_smda')
        elif self.request.user.groups.filter(name='grAdmin').exists():
            return redirect('admin')
        return response

    def get(self, request, *args, **kwargs):
        return render(request, 'login_user.html', {})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('login_user')
    template_name = 'password_change.html'

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        response = super().form_valid(form)
        user = form.save()
        user.profile.is_first_login = False
        user.profile.save()
        return response

    def form_invalid(self, form):
        # Capture specific validation errors and display them in the message
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('login_user')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        messages.success(self.request, "Your password has been reset successfully. You can now log in with your new password.")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login_user')

class ListMaterial_IL_View(grIL_GroupRequiredMixin, ListView):
    model = Material
    template_name = 'il/list_material_il.html'

    def get_context_data(self, **kwargs):
#        logger.info("This is an info message")
#        logger.error("This is an error message")
#        logger.warning("This is a warning message")
#        logger.critical("This is a critical message")
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
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' übermittelt.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' gelöscht.")
                selected_materials.delete()
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' archiviert.")

        return redirect(reverse('list_material_il'))

class AddMaterial_IL_View(FormValidMixin, grIL_GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'il/add_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list_material_il')
    success_message = "Das Material wurde erfolgreich hinzugefügt."

class UpdateMaterial_IL_View(FormValidMixin, grIL_GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'il/update_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list_material_il')
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
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' übermittelt.")
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' archiviert.")
            elif action == 'unarchive':
                selected_materials.update(is_archived=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' unarchiviert.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' gelöscht.")
                selected_materials.delete()
            elif action == 'export':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' exportiert.")
                return export_to_excel(selected_materials)

        return redirect(reverse('list_material_gd'))

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
    success_url = reverse_lazy('list_material_gd')
    success_message = "Das Material wurde erfolgreich aktualisiert."

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
        list_material_archived_smda = Material.objects.filter(is_transferred=True, is_archived=True)
        list_material_smda = Material.objects.filter(is_transferred=True, is_archived=False)

        # Convert positions_nr to integers for sorting
        context['list_material_archived_smda'] = sorted(list_material_archived_smda, key=lambda x: int(x.positions_nr))
        context['list_material_smda'] = sorted(list_material_smda, key=lambda x: int(x.positions_nr))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=False, transfer_date=timezone.now())
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' übermittelt.")
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' archiviert.")
            elif action == 'unarchive':
                selected_materials.update(is_archived=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' unarchiviert.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' gelöscht.")
                selected_materials.delete()
            elif action == 'export':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.username + "' exportiert.")
                return export_to_excel(selected_materials)

        return redirect(reverse('list_material_smda'))

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
    success_url = reverse_lazy('list_material_smda')
    success_message = "Das Material wurde erfolgreich aktualisiert."

    def form_valid(self, form):
        item = form.save(commit=False)
        if item.werkzuordnung_1 == "0800":
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

class Admin_View(ListView):
    template_name = 'admin.html'

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # First query: Get the number of materials
            cursor.execute("SELECT COUNT(*) FROM b11_1_material")
            nb_materials = cursor.fetchone()[0]

            # Second query: Get all log entries
            cursor.execute("SELECT * FROM b11_1_log_entries ORDER BY timestamp DESC")
            rows = cursor.fetchall()

            # Get column names from cursor description
            columns = [col[0] for col in cursor.description]

            # Convert rows to a list of dictionaries
            log_entries = [dict(zip(columns, row)) for row in rows]
            nb_log_entries = len(log_entries)

        # Context data to pass to the template
        context = { 
            'nb_materials': nb_materials,
            'nb_log_entries': nb_log_entries,
            'log_entries': log_entries,
        }
        return render(request, self.template_name, context)

