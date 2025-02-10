from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Material, Zuteilung, Auspraegung, G_Partner, MaterialAttachment
from .forms_il import MaterialForm_IL
from .forms_gd import MaterialForm_GD
from .forms_smda import MaterialForm_SMDA
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .mixins import grIL_GroupRequiredMixin, GroupRequiredMixin, grAdmin_GroupRequiredMixin, ComputedContextMixin
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
from .mixins import FormValidMixin_IL, FormValidMixin_GD, FormValidMixin_SMDA
from django.template import RequestContext
from .forms import CustomPasswordChangeForm
from .forms import CustomPasswordResetForm
from symm.models import Profile, Material
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .editable_fields_config import EDITABLE_FIELDS_GD, EDITABLE_FIELDS_SMDA, EDITABLE_FIELDS_IL
from django.views.generic.edit import FormView
from django import forms
from .import_utils import import_from_excel
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import UserRegistrationForm
import logging

logger = logging.getLogger(__name__)


class ExcelUploadForm(grAdmin_GroupRequiredMixin, forms.Form):
    """
    Form for uploading Excel files with material data.
    """
    excel_file = forms.FileField(
        label='Select Excel File',
        help_text='Upload an Excel file containing material data (.xlsx format)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx'
        })
    )

class ExcelImportView(GroupRequiredMixin, FormView):
    """
    View for handling Excel file uploads and importing material data.
    """
    allowed_groups = ['grLBA', 'grGD', 'grSMDA', 'grAdmin']
    template_name = 'admin/excel_import.html'
    form_class = ExcelUploadForm
    success_url = reverse_lazy('import_excel')

    def form_valid(self, form):
        excel_file = form.cleaned_data['excel_file']
        success, message, created, updated = import_from_excel(excel_file, self.request)

        if success:
            messages.success(self.request, message)
            logger.info(f"Import from '{excel_file}' by '{self.request.user.username}' successful.")
        else:
            messages.error(self.request, message)
            logger.warn(f"Error when importing '{excel_file}' by '{self.request.user.username}'.")
            return self.form_invalid(form)

        return super().form_valid(form)

def custom_permission_denied_view(request, exception=None):
    response = render(request, 'admin/403.html')
    response.status_code = 403
    return response

def home(request):
   return redirect('login_user')

class CustomLoginView(LoginView):
    template_name = 'admin/login_user.html'

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
#                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
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
        elif self.request.user.groups.filter(name='grLBA').exists():
            return redirect('list_material_gd')
        elif self.request.user.groups.filter(name='grAdmin').exists():
            return redirect('logging')
        return response

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/login_user.html', {})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('login_user')
    template_name = 'admin/password_change.html'

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        response = super().form_valid(form)
        user = form.save()
        user.profile.is_first_login = False
        user.profile.save()
        logger.info(f'User {user.username} changed his password.')
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
    template_name = 'admin/password_reset_confirm.html'

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

class ListMaterial_IL_View(GroupRequiredMixin, ListView):
    model = Material
    template_name = 'il/list_material_il.html'
    allowed_groups = ['grIL']

    def get_context_data(self, **kwargs):
#        logger.info("This is an info message")
#        logger.error("This is an error message")
#        logger.warning("This is a warning message")
#        logger.critical("This is a critical message")
        context = super().get_context_data(**kwargs)
        list_material_il = Material.objects.filter(is_transferred=False, hersteller=self.request.user, transfer_date__isnull=True)
        list_material_il_transferred = Material.objects.filter(is_transferred=True, hersteller=self.request.user, transfer_date__isnull=False)
        list_material_il_returned = Material.objects.filter(is_transferred=False, hersteller=self.request.user, transfer_date__isnull=False)

        print("len(list_material_il_transferred) = ", len(list_material_il_transferred))
        print("len(list_material_il_returned) = ", len(list_material_il_returned))
        print("len(list_material_il) = ", len(list_material_il))

        # Convert positions_nr to integers for sorting
        context['list_material_il'] = sorted(list_material_il, key=lambda x: int(x.positions_nr))
        context['list_material_il_transferred'] = sorted(list_material_il_transferred, key=lambda x: int(x.positions_nr))
        context['list_material_il_returned'] = sorted(list_material_il_returned, key=lambda x: int(x.positions_nr))
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

# In views.py
class AddMaterial_IL_View(FormValidMixin_IL, GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'il/add_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list_material_il')
    success_message = "Das Material wurde erfolgreich hinzugefügt."
    allowed_groups = ['grIL']

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            # Log the cancellation action
            self.object = self.get_object()
            logger.info(f"Bearbeitung von Material '{self.object.kurztext_de}' durch '{request.user.username}' abgebrochen.")
            return redirect('list_material_il')

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save the material instance
        self.object = form.save()
        
        # Handle file attachments
        files = self.request.FILES.getlist('attachment_files[]')
        comments = self.request.POST.getlist('attachment_comments[]')
        
        # Create MaterialAttachment instances for each file
        for file, comment in zip(files, comments):
            if file:  # Only create if a file was actually uploaded
                MaterialAttachment.objects.create(
                    material=self.object,
                    file=file,
                    comment=comment,
                    uploaded_by=self.request.user
                )
        
        return super().form_valid(form)

class UpdateMaterial_IL_View(FormValidMixin_IL, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'il/update_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list_material_il')
    success_message = "Das Material wurde erfolgreich aktualisiert."
    allowed_groups = ['grIL']

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            # Log the cancellation action
            self.object = self.get_object()
            logger.info(f"Bearbeitung von Material '{self.object.kurztext_de}' durch '{request.user.username}' abgebrochen.")
            return redirect('list_material_il')

        # Get the existing object
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save the material instance
        self.object = form.save()
        
        # Handle deletion of existing attachments
        attachments_to_delete = self.request.POST.getlist('delete_attachments[]')
        if attachments_to_delete:
            MaterialAttachment.objects.filter(
                id__in=attachments_to_delete,
                material=self.object
            ).delete()
            
        # Handle new file attachments
        files = self.request.FILES.getlist('attachment_files[]')
        comments = self.request.POST.getlist('attachment_comments[]')
        
        # Create MaterialAttachment instances for each new file
        for file, comment in zip(files, comments):
            if file:  # Only create if a file was actually uploaded
                MaterialAttachment.objects.create(
                    material=self.object,
                    file=file,
                    comment=comment,
                    uploaded_by=self.request.user
                )
        
        # Log the update action
        logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.username}' aktualisiert.")
        
        return super().form_valid(form)

class ShowMaterial_IL_View(GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'il/show_material_il.html'
    form_class = MaterialForm_IL
    allowed_groups = ['grIL']

    def post(self, request, *args, **kwargs):
        return redirect('list_material_il')

class ListMaterial_GD_View(ComputedContextMixin, GroupRequiredMixin, ListView):
    model = Material
    template_name = 'gd/list_material_gd.html'
    allowed_groups = ['grLBA', 'grGD']

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
        list_material_gd_archived = Material.objects.filter(is_transferred=True, is_archived=True)
        list_material_gd = Material.objects.filter(is_transferred=True, is_archived=False)

        # Convert positions_nr to integers for sorting
        context['list_material_gd_archived'] = sorted(list_material_gd_archived, key=lambda x: int(x.positions_nr))
        context['list_material_gd'] = sorted(list_material_gd, key=lambda x: int(x.positions_nr))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        print("len(selected_material_ids) = ", str(len(selected_material_ids)))
        # To switch from LBA mode to RUAG mode
        export_type = request.POST.get('export_type')
        action = request.POST.get('action')
        print("action = ", action)

        if selected_material_ids and action:
            print("**** post()")
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                transfer_comment = request.POST.get('transfer_comment', '')
                selected_materials.update(is_transferred=False, transfer_date=timezone.now(), transfer_comment=transfer_comment)
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
                return export_to_excel(selected_materials, export_type)

        return redirect(reverse('list_material_gd'))

class ListMaterialArchived_GD_View(GroupRequiredMixin, ListView):
    model = Material
    template_name = 'gd/list_material_gd_archived.html'
    context_object_name = 'list_material_gd_archived'
    allowed_groups = ['grLBA', 'grGD']

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

class UpdateMaterial_GD_View(ComputedContextMixin, FormValidMixin_GD, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'gd/update_material_gd.html'
    form_class = MaterialForm_GD
    success_url = reverse_lazy('list_material_gd')
    success_message = "Das Material wurde erfolgreich aktualisiert."
    allowed_groups = ['grLBA', 'grGD']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['editable_fields'] = EDITABLE_FIELDS_GD
        return kwargs

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            # Log the cancellation action
            self.object = self.get_object()
            logger.info(f"Bearbeitung von Material '{self.object.kurztext_de}' durch '{request.user.username}' abgebrochen.")
            return redirect('list_material_gd')

        # Get the existing object
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save the material instance
        self.object = form.save()
        
        # Handle deletion of existing attachments
        attachments_to_delete = self.request.POST.getlist('delete_attachments[]')
        if attachments_to_delete:
            MaterialAttachment.objects.filter(
                id__in=attachments_to_delete,
                material=self.object
            ).delete()
            
        # Handle new file attachments
        files = self.request.FILES.getlist('attachment_files[]')
        comments = self.request.POST.getlist('attachment_comments[]')
        
        # Create MaterialAttachment instances for each new file
        for file, comment in zip(files, comments):
            if file:  # Only create if a file was actually uploaded
                MaterialAttachment.objects.create(
                    material=self.object,
                    file=file,
                    comment=comment,
                    uploaded_by=self.request.user
                )
        
        # Log the update action
        logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.username}' aktualisiert.")
        
        return super().form_valid(form)

class ShowMaterial_GD_View(ComputedContextMixin, GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'gd/show_material_gd.html'
    form_class = MaterialForm_GD
    allowed_groups = ['grLBA', 'grGD']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context    

    def post(self, request, *args, **kwargs):
        return redirect('list_material_gd')

class ListMaterial_SMDA_View(ComputedContextMixin, GroupRequiredMixin, ListView):
    model = Material
    template_name = 'smda/list_material_smda.html'
    allowed_groups = ['grLBA', 'grSMDA']

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
        list_material_smda_archived = Material.objects.filter(is_transferred=True, is_archived=True)
        list_material_smda = Material.objects.filter(is_transferred=True, is_archived=False)

        # Convert positions_nr to integers for sorting
        context['list_material_smda_archived'] = sorted(list_material_smda_archived, key=lambda x: int(x.positions_nr))
        context['list_material_smda'] = sorted(list_material_smda, key=lambda x: int(x.positions_nr))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        # To switch from LBA mode to RUAG mode
        export_type = request.POST.get('export_type')
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
                return export_to_excel(selected_materials, export_type)

        return redirect(reverse('list_material_smda'))

class ListMaterialArchived_SMDA_View(GroupRequiredMixin, ListView):
    model = Material
    template_name = 'smda/list_material_smda_archived.html'
    context_object_name = 'list_material_smda_archived'
    allowed_groups = ['grLBA', 'grSMDA']

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

class UpdateMaterial_SMDA_View(ComputedContextMixin, FormValidMixin_SMDA, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'smda/update_material_smda.html'
    form_class = MaterialForm_SMDA
    success_url = reverse_lazy('list_material_smda')
    success_message = "Das Material wurde erfolgreich aktualisiert."
    allowed_groups = ['grLBA', 'grSMDA']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['editable_fields'] = EDITABLE_FIELDS_SMDA
        return kwargs

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            # Log the cancellation action
            self.object = self.get_object()
            logger.info(f"Bearbeitung von Material '{self.object.kurztext_de}' durch '{request.user.username}' abgebrochen.")
            return redirect('list_material_smda')

        # Get the existing object
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save the material instance
        self.object = form.save()
        
        # Handle deletion of existing attachments
        attachments_to_delete = self.request.POST.getlist('delete_attachments[]')
        if attachments_to_delete:
            MaterialAttachment.objects.filter(
                id__in=attachments_to_delete,
                material=self.object
            ).delete()
            
        # Handle new file attachments
        files = self.request.FILES.getlist('attachment_files[]')
        comments = self.request.POST.getlist('attachment_comments[]')
        
        # Create MaterialAttachment instances for each new file
        for file, comment in zip(files, comments):
            if file:  # Only create if a file was actually uploaded
                MaterialAttachment.objects.create(
                    material=self.object,
                    file=file,
                    comment=comment,
                    uploaded_by=self.request.user
                )
        
        # Log the update action
        logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.username}' aktualisiert.")
        
        return super().form_valid(form)

class ShowMaterial_SMDA_View(ComputedContextMixin, GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'smda/show_material_smda.html'
    form_class = MaterialForm_SMDA
    allowed_groups = ['grLBA', 'grSMDA']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context    

    def post(self, request, *args, **kwargs):
        return redirect('list_material_smda')

class Logging_View(ListView):
    template_name = 'admin/logging.html'

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # First query: Get the number of materials
            cursor.execute("SELECT COUNT(*) FROM symm_material")
            nb_materials = cursor.fetchone()[0]

            # Second query: Get all log entries
            cursor.execute("SELECT * FROM symm_log_entries ORDER BY timestamp DESC")
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

class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            submitted_username = form.cleaned_data['username']
            
            user = User.objects.create(
                username=submitted_username,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_active=False
            )

            profile = form.save(commit=False)
            profile.user = user
            profile.username = submitted_username
            profile.registration_token = get_random_string(50)
            profile.token_expiry = timezone.now() + timedelta(days=2)
            profile.status = 'pending'  # Set initial status
            profile.save()

            messages.success(request, 'Registration submitted successfully! Please wait for administrator approval.')
            logger.info(f"New user registration pending approval: {submitted_username}")
            return redirect('login_user')

        return render(request, self.template_name, {'form': form})

class CompleteRegistrationView(View):
    template_name = 'registration/complete_registration.html'

    def get(self, request, token):
        try:
            profile = Profile.objects.get(
                registration_token=token,
                token_expiry__gt=timezone.now(),
                user__is_active=False
            )
            return render(request, self.template_name, {'token': token})
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid or expired registration link.')
            return redirect('login_user')

    def post(self, request, token):
        try:
            profile = Profile.objects.get(
                registration_token=token,
                token_expiry__gt=timezone.now(),
                user__is_active=False
            )

            password = request.POST.get('password')
            if password:
                user = profile.user
                # Remove this line as we want to keep the original username
                # user.username = profile.email  # This was causing the issue
                user.set_password(password)
                user.is_active = True
                user.save()
                
                profile.registration_token = None
                profile.token_expiry = None
                profile.save()
                
                messages.success(request, 'Registration completed! You can now login.')
                return redirect('login_user')
            else:
                messages.error(request, 'Please provide a password.')
                
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid or expired registration link.')

        return render(request, self.template_name, {'token': token})

class PendingRegistrationsView(grAdmin_GroupRequiredMixin, ListView):
    model = Profile
    template_name = 'admin/pending_registrations.html'
    context_object_name = 'pending_profiles'
    allowed_groups = ['grAdmin']

    def get_queryset(self):
        return Profile.objects.filter(status='pending').order_by('-registration_date')

class ApproveRegistrationView(grAdmin_GroupRequiredMixin, View):
    allowed_groups = ['grAdmin']

    def post(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id, status='pending')
            user = profile.user

            # Approve the user
            profile.status = 'approved'
            profile.save()

            # Add user to grIL group
            try:
                il_group = Group.objects.get(name='grIL')
                user.groups.add(il_group)
            except Group.DoesNotExist:
                logger.error(f"Group 'grIL' not found when approving user {profile.username}")

            # Send approval email
            registration_link = request.build_absolute_uri(
                reverse('complete_registration', args=[profile.registration_token])
            )

            email_context = {
                'username': profile.username,
                'registration_link': registration_link,
                'expiry_date': profile.token_expiry,
            }

            email_body = render_to_string('registration/email/registration_approved_email.html', email_context)

#            send_mail(
#                'Your registration has been approved',
#                email_body,
#                settings.DEFAULT_FROM_EMAIL,
#                [profile.email],
#                fail_silently=False,
#            )
            print("[ApproveRegistrationView] Mail sent!")
            print("email_body = ", email_body)

            messages.success(request, f'Registration for {profile.username} has been approved.')
            logger.info(f"Registration approved for user: {profile.username}")

        except Profile.DoesNotExist:
            messages.error(request, 'Profile not found.')

        return redirect('pending_registrations')

class RejectRegistrationView(grAdmin_GroupRequiredMixin, View):
    allowed_groups = ['grAdmin']

    def post(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id, status='pending')
            rejection_reason = request.POST.get('rejection_reason')

            if not rejection_reason:
                messages.error(request, 'Please provide a rejection reason.')
                return redirect('pending_registrations')

            # Reject the user
            profile.status = 'rejected'
            profile.rejection_reason = rejection_reason
            profile.save()

            # Send rejection email
            email_context = {
                'username': profile.username,
                'rejection_reason': rejection_reason,
            }

            email_body = render_to_string('registration/email/registration_rejected_email.html', email_context)

#            send_mail(
#                'Your registration has been rejected',
#                email_body,
#                settings.DEFAULT_FROM_EMAIL,
#                [profile.email],
#                fail_silently=False,
#            )
            print("[RejectRegistrationView] Mail sent!")
            print("email_body = ", email_body)

            # Delete the associated User object
            profile.user.delete()

            messages.success(request, f'Registration for {profile.username} has been rejected.')
            logger.info(f"Registration rejected for user: {profile.username}")

        except Profile.DoesNotExist:
            messages.error(request, 'Profile not found.')

        return redirect('pending_registrations')
