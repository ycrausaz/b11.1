# views.py

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Material, Zuteilung, Auspraegung, G_Partner, MaterialAttachment
from .forms.forms_il import MaterialForm_IL
from .forms.forms_gd import MaterialForm_GD
from .forms.forms_smda import MaterialForm_SMDA
from .forms.forms_lba import MaterialForm_LBA
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .utils.mixins import grIL_GroupRequiredMixin, GroupRequiredMixin, grAdmin_GroupRequiredMixin, ComputedContextMixin
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
from .utils.export_utils import export_to_excel
from django.contrib import messages
import re
from .utils.mixins import FormValidMixin
from django.template import RequestContext
from .forms.forms import CustomPasswordChangeForm
from .forms.forms import CustomPasswordResetForm
from .forms.forms import EmailVerificationForm
from .forms.forms import RegistrationPasswordForm
from b11_1.models import Profile, Material
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
from .utils.editable_fields_config import (
    EDITABLE_FIELDS_IL,
    EDITABLE_FIELDS_IL_TABULAR_MASS_UPDATE,
    EDITABLE_FIELDS_IL_MASS_UPDATE,
    EDITABLE_FIELDS_LBA,
    EDITABLE_FIELDS_GD,
    EDITABLE_FIELDS_SMDA
)
from django.views.generic.edit import FormView
from django import forms
from .utils.import_utils import import_from_excel
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms.forms import UserRegistrationForm
from django.db import transaction
from django.core.exceptions import ValidationError
from botocore.exceptions import BotoCoreError, ClientError
from .utils.log_export_utils import export_logs_to_excel
import logging

logger = logging.getLogger(__name__)

class ExcelUploadForm(forms.Form):
    """
    Form for uploading Excel files with material data.
    """
    excel_file = forms.FileField(
        label='Excel-Datei auswählen',
        help_text='Eine Excel-Datei mit Materialien (.xlsx format) hochladen',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx'
        })
    )
    
    il_user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='grIL'),
        label='Zuweisung',
        help_text='Wählen Sie den Benutzer aus, der als Hersteller zugewiesen werden soll (erforderlich).',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=True,
        error_messages={'obligatorisch': 'Bitte wählen Sie einen IL-Benutzer, um fortzufahren.'}
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up the queryset to show email as display value
        self.fields['il_user'].label_from_instance = lambda obj: obj.email

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
        il_user = form.cleaned_data['il_user']  # Get the selected user
        
        success, message, created, updated = import_from_excel(excel_file, self.request, il_user)

        if success:
            messages.success(self.request, message)
            logger.info(f"Import from '{excel_file}' by '{self.request.user.email}' successful. Assigned to IL user: {il_user.email}")
        else:
            messages.error(self.request, message)
            logger.warn(f"Error when importing '{excel_file}' by '{self.request.user.email}'.")
            return self.form_invalid(form)

        return super().form_valid(form)

def custom_permission_denied_view(request, exception=None):
    response = render(request, 'admin/403.html')
    response.status_code = 403
    return response

def home(request):
   return redirect('login_user')

class PreRegisterView(FormView):
    """
    Initial view for email verification
    """
    template_name = 'registration/pre_register.html'
    form_class = EmailVerificationForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('verified_email')
        context['recaptcha_site_key'] = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', 'dummy_key')
        context['settings'] = settings  # Pass settings to template
        return context
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        # Generate verification token
        verification_token = get_random_string(64)
        
        # Store token in session for validation later
        self.request.session['email_verification'] = {
            'email': email,
            'token': verification_token,
            'expires': (timezone.now() + timedelta(hours=24)).isoformat()
        }
        
        # Generate verification link
        current_site = get_current_site(self.request)
        verification_link = f"http://{current_site.domain}{reverse('verify_email')}?email={email}&token={verification_token}"
        
        # Prepare email context
        email_context = {
            'verification_link': verification_link,
            'expiry_date': (timezone.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        # Render email template
        email_body = render_to_string('registration/email/verification_email.html', email_context)
        
        # In development environment - print details to console instead of sending email
        print("\n" + "="*80)
        print("DEVELOPMENT MODE: Email Verification")
        print("="*80)
        print(f"To: {email}")
        print(f"Subject: Verify your email address")
        print("-"*80)
        print(email_body)
        print("-"*80)
        print(f"VERIFICATION LINK: {verification_link}")
        print("="*80 + "\n")
        
        # Log the verification link for easy access
        logger.info(f"Verification link for {email}: {verification_link}")
        
        # Add success message
        messages.success(self.request, "Verification email sent! Please check your inbox to continue registration.")
        
        return redirect('login_user')

class VerifyEmailView(View):
    """
    Email verification handler
    """
    def get(self, request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        
        # Get verification data from session
        verification_data = request.session.get('email_verification', {})
        
        # Debug info
        print("\n" + "="*80)
        print("DEBUG: Email Verification Attempt")
        print(f"Email in URL: {email}")
        print(f"Token in URL: {token}")
        print(f"Session verification data: {verification_data}")
        print("="*80 + "\n")
        
        if not verification_data:
            messages.error(request, "Verification link is invalid or has expired. (Session data not found)")
            return redirect('pre_register')
        
        # Verify token and email
        stored_email = verification_data.get('email')
        stored_token = verification_data.get('token')
        expires = verification_data.get('expires')
        
        print("\n" + "="*80)
        print("DEBUG: Verification Comparison")
        print(f"Stored email: {stored_email} | Matches: {stored_email == email}")
        print(f"Stored token: {stored_token} | Matches: {stored_token == token}")
        
        if expires:
            expiry_time = timezone.datetime.fromisoformat(expires)
            is_expired = timezone.now() > expiry_time
            print(f"Expiry time: {expiry_time} | Expired: {is_expired}")
        else:
            print("No expiry time found")
        print("="*80 + "\n")
        
        if (stored_email != email or 
            stored_token != token or
            (expires and timezone.now() > timezone.datetime.fromisoformat(expires))):
            
            messages.error(request, "Verification link is invalid or has expired. (Data mismatch)")
            return redirect('pre_register')
        
        # Log successful verification
        logger.info(f"Email verification successful for: {email}")
        
        # Store verified email in the session (mark it as verified)
        self.request.session['verified_email'] = email
        self.request.session.modified = True

        # Add these debug lines
        print("\n" + "="*80)
        print("DEBUG: Session after storing verified_email")
        print(f"verified_email in session: {self.request.session.get('verified_email')}")
        print(f"Full session data: {dict(self.request.session)}")
        print(f"Session key: {self.request.session.session_key}")
        print("="*80 + "\n")
        
        # Redirect to registration form without email parameter
        return redirect('register')

class CustomLoginView(LoginView):
    template_name = 'admin/login_user.html'

    def form_valid(self, form):
        # Get the authenticated user
        user = form.get_user()

        # Check the user's profile status
        try:
            profile = user.profile

            # Check if status is 'pending'
            if profile.status == 'pending':
                messages.error(
                    self.request,
                    "Your account is pending approval. Please wait for an administrator to approve your registration."
                )
                logger.info(f"Login attempt from pending user: {user.email}")
                return self.render_to_response(self.get_context_data(form=form))

            # Check if status is 'rejected'
            elif profile.status == 'rejected':
                messages.error(
                    self.request,
                    f"Your registration has been rejected."
                )
                logger.info(f"Login attempt from rejected user: {user.email}")
                return self.render_to_response(self.get_context_data(form=form))

            # If status is 'approved', proceed with login
            elif profile.status == 'approved':
                # Normal login flow for approved users
                response = super().form_valid(form)
                profile.failed_login_attempts = 0  # Reset failed attempts on successful login
                profile.save()

                # Your existing redirection logic
                if self.request.user.groups.filter(name='grIL').exists():
                    return redirect('list_material_il')
                elif self.request.user.groups.filter(name='grGD').exists():
                    return redirect('list_material_gd')
                elif self.request.user.groups.filter(name='grSMDA').exists():
                    return redirect('list_material_smda')
                elif self.request.user.groups.filter(name='grLBA').exists():
                    return redirect('list_material_lba')
                elif self.request.user.groups.filter(name='grAdmin').exists():
                    return redirect('logging')

                return response

            # Handle unexpected status values
            else:
                messages.error(
                    self.request,
                    "Your account has an unknown status. Please contact an administrator."
                )
                logger.warning(f"Login attempt from user with unknown status '{profile.status}': {user.email}")
                return self.render_to_response(self.get_context_data(form=form))

        except Profile.DoesNotExist:
            # Handle users without profiles
            messages.error(
                self.request,
                "Account configuration issue. Please contact the administrator."
            )
            logger.error(f"User without profile attempted login: {user.email}")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """
        Handle invalid login attempts without showing duplicate error messages
        """
        username_field = form.cleaned_data.get('username')

        # First check if this is a user in our system with a special status
        if username_field:
            try:
                user = User.objects.get(email=username_field)

                # If user exists, check their profile status
                try:
                    profile = user.profile

                    # If the password is incorrect, handle failed attempts
                    profile.failed_login_attempts += 1
                    profile.save()

                    # If too many failed attempts, send password reset link
                    if profile.failed_login_attempts >= 3:
                        current_site = get_current_site(self.request)
                        mail_subject = 'Reset your password'
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token = default_token_generator.make_token(user)
                        reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                        reset_url = f'http://{current_site.domain}{reset_link}'
                        message = f'It seems you have failed to login 3 times. Please reset your password using the following link:\n{reset_url}'
                        # Uncomment to enable sending emails
                        # send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                        logger.info(f'Password reset email sent to user: {user.email}')
                        logger.info(message)

                        messages.warning(
                            self.request,
                            "You have entered an incorrect password 3 times. "
                            "A password reset link has been sent to your email."
                        )

                        profile.failed_login_attempts = 0
                        profile.save()
                        return self.render_to_response(self.get_context_data(form=form))

                except Profile.DoesNotExist:
                    # User exists but profile doesn't
                    logger.error(f"User without profile attempted login: {username_field}")

            except User.DoesNotExist:
                # User doesn't exist
                pass

        # For all other cases, show the standard error message
        messages.error(self.request, "Email und/oder Passwort ungültig.")
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/login_user.html', {})

class ExportLogsView(GroupRequiredMixin, View):
    """
    View for exporting log entries to Excel with date filtering
    """
    allowed_groups = ['grAdmin']

    def get(self, request, *args, **kwargs):
        from datetime import datetime
        
        # Get date filter parameters
        raw_start_date = request.GET.get('start_date')
        raw_end_date = request.GET.get('end_date')
        
        # Initialize date variables
        start_date = None
        end_date = None
        
        # Parse start date if provided
        if raw_start_date:
            try:
                formats_to_try = ['%Y-%m-%d', '%d.%m.%Y']
                for date_format in formats_to_try:
                    try:
                        start_date = datetime.strptime(raw_start_date, date_format).date()
                        break
                    except ValueError:
                        continue
            except Exception as e:
                logger.error(f"Error parsing start_date '{raw_start_date}': {e}")
        
        # Parse end date if provided
        if raw_end_date:
            try:
                formats_to_try = ['%Y-%m-%d', '%d.%m.%Y']
                for date_format in formats_to_try:
                    try:
                        end_date = datetime.strptime(raw_end_date, date_format).date()
                        break
                    except ValueError:
                        continue
            except Exception as e:
                logger.error(f"Error parsing end_date '{raw_end_date}': {e}")
        
        # Generate Excel file and return as response
        response = export_logs_to_excel(start_date, end_date)
        
        # Log the export action
        logger.info(f"Log entries exported to Excel by {request.user.email} (date range: {start_date} to {end_date})")
        
        return response

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('login_user')
    template_name = 'admin/password_change.html'

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        response = super().form_valid(form)
        user = form.save()
#        user.profile.is_first_login = False
        user.profile.save()
        logger.info(f'User {user.email} changed his password.')
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
    template_name = 'admin/password_change.html'

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
        context = super().get_context_data(**kwargs)
        list_material_il = Material.objects.filter(is_transferred=False, hersteller=self.request.user.email, transfer_date__isnull=True)
        list_material_il_transferred = Material.objects.filter(is_transferred=True, hersteller=self.request.user.email, transfer_date__isnull=False)
        list_material_il_returned = Material.objects.filter(is_transferred=False, hersteller=self.request.user.email, transfer_date__isnull=False)

#        print("len(list_material_il_transferred) = ", len(list_material_il_transferred))
#        print("len(list_material_il_returned) = ", len(list_material_il_returned))
#        print("len(list_material_il) = ", len(list_material_il))

        # Define sort key function that handles None values
        def sort_key(x):
            if x.positions_nr is None:
                return float('inf')  # Put None values at the end
            return int(x.positions_nr)

        # Sort lists using the new sort key
        context['list_material_il'] = sorted(list_material_il, key=sort_key)
        context['list_material_il_transferred'] = sorted(list_material_il_transferred, key=sort_key)
        context['list_material_il_returned'] = sorted(list_material_il_returned, key=sort_key)

        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                # Only transfer materials that are marked as finished
                finished_materials = Material.objects.filter(
                    id__in=selected_material_ids,
                    is_finished=True
                )
                
                # Count how many materials were selected vs. how many are finished
                total_selected = len(selected_material_ids)
                total_finished = finished_materials.count()
                
                # Update only the finished materials
                if total_finished > 0:
                    finished_materials.update(is_transferred=True, transfer_date=timezone.now())
                    for material in finished_materials:
                        logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' übermittelt.")
                    
                    # Add a message to inform the user
                    if total_finished < total_selected:
                        messages.warning(
                            request,
                            f"{total_finished} Material(ien) wurden übermittelt. {total_selected - total_finished} Material(ien) waren nicht als 'abgeschlossen' markiert und wurden nicht übermittelt."
                        )
                    else:
                        messages.success(
                            request,
                            f"{total_finished} Material(ien) wurden erfolgreich übermittelt."
                        )
                else:
                    # If no materials were finished, show a warning
                    messages.warning(
                        request,
                        "Keine Materialien wurden übermittelt, da keines als fertig markiert war."
                    )
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' gelöscht.")
                selected_materials.delete()
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' archiviert.")

        return redirect(reverse('list_material_il'))

class AddMaterial_IL_View(FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'il/add_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list_material_il')
    success_message = "Das Material wurde erfolgreich hinzugefügt."
    allowed_groups = ['grIL']

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Start by validating the form data
                self.object = form.save(commit=False)

                # Get new files and comments
                files = self.request.FILES.getlist('attachment_files[]')
                comments = self.request.POST.getlist('attachment_comments[]')

                # Create temporary list to track new attachments
                new_attachments = []

                # Process new file attachments
                for file, comment in zip(files, comments):
                    if file:
                        try:
                            attachment = MaterialAttachment(
                                material=self.object,
                                file=file,
                                comment=comment,
                                uploaded_by=self.request.user
                            )
                            # Validate the attachment
                            attachment.full_clean()

                            # Try to save file to S3 first
                            try:
                                # Note: Don't save to database yet
                                attachment.file.save(file.name, file, save=False)
                            except (BotoCoreError, ClientError) as e:
                                error_msg = f"Failed to upload file '{file.name}' to storage."
                                logger.error(error_msg)
                                form.add_error(None, error_msg)
                                return self.render_to_response(self.get_context_data(form=form))

                            new_attachments.append(attachment)

                        except ValidationError as e:
                            error_msg = f"Validation error for file {file.name}: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                # If we got here, all S3 operations were successful
                # Now save the material object
                self.object.save()

                # And save all new attachments to database
                for attachment in new_attachments:
                    attachment.save()

                # Log the successful creation
                logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.email}' erstellt.")

                return super().form_valid(form)

        except ValidationError as e:
            # Clean up any files that might have been uploaded to S3 before the error
            for attachment in new_attachments:
                try:
                    attachment.file.delete(save=False)
                except (BotoCoreError, ClientError) as s3_error:
                    logger.error(f"Failed to clean up file {attachment.file.name} after error: {str(s3_error)}")

            form.add_error(None, str(e))
            return self.render_to_response(self.get_context_data(form=form))

        except (BotoCoreError, ClientError) as e:
            error_msg = f"Failed to upload file to storage."
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

class UpdateMaterial_IL_View(FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'il/update_material_il.html'
    form_class = MaterialForm_IL
    success_url = reverse_lazy('list_material_il')
    success_message = "Das Material wurde erfolgreich aktualisiert."
    allowed_groups = ['grIL']

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Start by validating the form data
                self.object = form.save(commit=False)

                # Get new files and comments
                files = self.request.FILES.getlist('attachment_files[]')
                comments = self.request.POST.getlist('attachment_comments[]')
                attachments_to_delete = self.request.POST.getlist('delete_attachments[]')

                # Handle deletion of existing attachments first
                if attachments_to_delete:
                    attachments = MaterialAttachment.objects.filter(
                        id__in=attachments_to_delete,
                        material=self.object
                    )
                    for attachment in attachments:
                        try:
                            # Delete from S3 first
                            attachment.file.delete(save=False)
                        except (BotoCoreError, ClientError) as e:
                            error_msg = f"Failed to delete file {attachment.file.name} from storage: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                        # If S3 deletion successful, delete from database
                        attachment.delete()

                # Create temporary list to track new attachments
                new_attachments = []

                # Process new file attachments
                for file, comment in zip(files, comments):
                    if file:
                        try:
                            attachment = MaterialAttachment(
                                material=self.object,
                                file=file,
                                comment=comment,
                                uploaded_by=self.request.user
                            )
                            # Validate the attachment
                            attachment.full_clean()

                            # Try to save file to S3 first
                            try:
                                # Note: Don't save to database yet
                                attachment.file.save(file.name, file, save=False)
                            except (BotoCoreError, ClientError) as e:
                                error_msg = f"Failed to upload file '{file.name}' to storage."
                                logger.error(error_msg)
                                form.add_error(None, error_msg)
                                return self.render_to_response(self.get_context_data(form=form))

                            new_attachments.append(attachment)

                        except ValidationError as e:
                            error_msg = f"Validation error for file {file.name}: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                # If we got here, all S3 operations were successful
                # Now save the material object
                self.object.save()

                # And save all new attachments to database
                for attachment in new_attachments:
                    attachment.save()

                # Log the successful update
                logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.email}' aktualisiert.")

                return super().form_valid(form)

        except ValidationError as e:
            # Clean up any files that might have been uploaded to S3 before the error
            for attachment in new_attachments:
                try:
                    attachment.file.delete(save=False)
                except (BotoCoreError, ClientError) as s3_error:
                    logger.error(f"Failed to clean up file {attachment.file.name} after error: {str(s3_error)}")

            form.add_error(None, str(e))
            return self.render_to_response(self.get_context_data(form=form))

        except (BotoCoreError, ClientError) as e:
            error_msg = f"Failed to upload file to storage."
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

class MassUpdateMaterial_IL_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    template_name = 'il/mass_update_material_il.html'
    success_url = reverse_lazy('list_material_il')
    success_message = "Die Materialien wurden erfolgreich aktualisiert."
    allowed_groups = ['grIL']

    def get(self, request, *args, **kwargs):
        material_ids = request.GET.getlist('materials')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Massenbearbeitung ausgewählt.")
            return redirect('list_material_il')

        materials = Material.objects.filter(id__in=material_ids)
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_il')

        # Create form with editable fields configuration for IL mass update
        # IMPORTANT: Pass is_mass_update=True to disable default required field validation
        form = MaterialForm_IL(
            editable_fields=EDITABLE_FIELDS_IL_MASS_UPDATE,
            is_mass_update=True
        )

        context = {
            'form': form,
            'materials': materials,
            'material_count': materials.count(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        material_ids = request.POST.getlist('material_ids')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Massenbearbeitung ausgewählt.")
            return redirect('list_material_il')

        materials = Material.objects.filter(id__in=material_ids)
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_il')

        # Create form with mass update configuration
        form = MaterialForm_IL(
            request.POST, 
            editable_fields=EDITABLE_FIELDS_IL_MASS_UPDATE,
            is_mass_update=True
        )

        # Get which fields should be updated (those with checked checkboxes)
        fields_to_update = []
        for field_name in form.fields:
            checkbox_name = f"update_{field_name}"
            if request.POST.get(checkbox_name):
                fields_to_update.append(field_name)

        if not fields_to_update:
            messages.warning(request, "Keine Felder zum Aktualisieren ausgewählt.")
            context = {
                'form': form,
                'materials': materials,
                'material_count': materials.count(),
            }
            return render(request, self.template_name, context)

        # Custom validation for mass updates - only validate selected fields
        validation_errors = {}

        # Check each field that's being updated
        for field_name in fields_to_update:
            if field_name in form.fields:
                field = form.fields[field_name]
                raw_value = request.POST.get(field_name)

                # For required fields in the original Meta.required_fields, validate them
                if field_name in form.Meta.required_fields:
                    if not raw_value or (isinstance(raw_value, str) and raw_value.strip() == ''):
                        validation_errors[field_name] = ["Dieses Feld ist erforderlich."]

                # For foreign key fields, validate that the value exists
                if field_name in form.Meta.foreign_key_fields and raw_value:
                    try:
                        # Convert to int and check if it exists
                        if raw_value != '':
                            int(raw_value)
                    except (ValueError, TypeError):
                        validation_errors[field_name] = ["Ungültiger Wert ausgewählt."]

        # If there are validation errors, show them
        if validation_errors:
            for field_name, errors in validation_errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field_name].label}: {error}")

            context = {
                'form': form,
                'materials': materials,
                'material_count': materials.count(),
            }
            return render(request, self.template_name, context)

        # If validation passes, proceed with the update
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_count = 0
                    updated_fields = []

                    # Build the list of field names for logging
                    for field_name in fields_to_update:
                        if field_name not in updated_fields:
                            updated_fields.append(field_name)

                    # Update each material with the selected fields
                    for material in materials:
                        material_updated = False
                        for field_name in fields_to_update:
                            if field_name in form.cleaned_data:
                                new_value = form.cleaned_data[field_name]

                                # Set the field value directly
                                # The form's clean() method has already converted values to proper types
                                setattr(material, field_name, new_value)
                                material_updated = True

                        if material_updated:
                            material.save(update_fields=fields_to_update)
                            updated_count += 1
                            logger.info(f"Material '{material.kurztext_de}' wurde durch Massenbearbeitung von '{request.user.email}' aktualisiert. Felder: {', '.join(updated_fields)}")

                    if updated_count > 0:
                        messages.success(
                            request, 
                            f"{updated_count} Material(ien) wurden erfolgreich aktualisiert. "
                            f"Geänderte Felder: {', '.join(updated_fields)}"
                        )
                    else:
                        messages.warning(request, "Keine Materialien wurden aktualisiert.")

                    return redirect('list_material_il')

            except Exception as e:
                error_msg = f"Fehler bei der Massenbearbeitung: {str(e)}"
                logger.error(error_msg)
                messages.error(request, error_msg)

        else:
            # Form has errors - but only show errors for fields that were actually being updated
            for field_name, errors in form.errors.items():
                if field_name in fields_to_update:
                    for error in errors:
                        messages.error(request, f"{form.fields.get(field_name, {}).get('label', field_name)}: {error}")

        # If we get here, there were errors - redisplay the form
        context = {
            'form': form,
            'materials': materials,
            'material_count': materials.count(),
        }
        return render(request, self.template_name, context)

class TabularMaterialsMassUpdateMaterial_LBA_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    template_name = 'lba/tabular_materials_mass_update_material_lba.html'
    success_url = reverse_lazy('list_material_lba')
    success_message = "Die Materialien wurden erfolgreich aktualisiert."
    allowed_groups = ['grLBA']

class TabularMaterialsMassUpdateMaterial_IL_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    template_name = 'il/tabular_materials_mass_update_material_il.html'
    success_url = reverse_lazy('list_material_il')
    success_message = "Die Materialien wurden erfolgreich aktualisiert."
    allowed_groups = ['grIL']

    def get(self, request, *args, **kwargs):
        material_ids = request.GET.getlist('materials')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Tabellen-Massenbearbeitung ausgewählt.")
            return redirect('list_material_il')

        materials = Material.objects.filter(id__in=material_ids).order_by('positions_nr')
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_il')

        # Create a modified field list excluding 'systemname'
        tabular_editable_fields = [field for field in EDITABLE_FIELDS_IL_TABULAR_MASS_UPDATE if field != 'systemname']

        # Create a form for each material
        material_forms = []
        for material in materials:
            form = MaterialForm_IL(
                instance=material,
                editable_fields=tabular_editable_fields,  # Use the modified list
                is_mass_update=True,
                prefix=f'material_{material.id}'
            )
            material_forms.append({
                'material': material,
                'form': form
            })

        # Get field information for the table headers using the modified list
        sample_form = MaterialForm_IL(
            editable_fields=tabular_editable_fields,  # Use the modified list
            is_mass_update=True
        )
        
        # Get only the normal (editable) fields
        editable_fields = []
        for field in sample_form.get_normal_fields():
            if not field.is_hidden:
                editable_fields.append({
                    'name': field.name,
                    'label': field.label,
                    'required': field.name in sample_form.get_required_field_names(),
                    'help_text': field.help_text
                })

        context = {
            'material_forms': material_forms,
            'materials': materials,
            'material_count': materials.count(),
            'editable_fields': editable_fields,
        }
        return render(request, self.template_name, context)

    # Also update the post method to use the same filtered fields
    def post(self, request, *args, **kwargs):
        material_ids = request.POST.getlist('material_ids')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Tabellen-Massenbearbeitung ausgewählt.")
            return redirect('list_material_il')

        materials = Material.objects.filter(id__in=material_ids).order_by('positions_nr')
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_il')

        # Use the same filtered field list
        tabular_editable_fields = [field for field in EDITABLE_FIELDS_IL_TABULAR_MASS_UPDATE if field != 'systemname']

        # Create forms for each material with POST data
        material_forms = []
        all_forms_valid = True
        
        for material in materials:
            form = MaterialForm_IL(
                request.POST,
                instance=material,
                editable_fields=tabular_editable_fields,  # Use the modified list
                is_mass_update=True,
                prefix=f'material_{material.id}'
            )
            material_forms.append({
                'material': material,
                'form': form
            })
            
            if not form.is_valid():
                all_forms_valid = False

        # Rest of the post method remains the same...
        if all_forms_valid:
            try:
                with transaction.atomic():
                    updated_count = 0
                    
                    for material_form_data in material_forms:
                        form = material_form_data['form']
                        material = material_form_data['material']
                        
                        # Check if any field has actually changed
                        form_changed = False
                        for field_name in form.changed_data:
                            if field_name in tabular_editable_fields:  # Use the modified list
                                form_changed = True
                                break
                        
                        if form_changed:
                            form.save()
                            updated_count += 1
                            logger.info(f"Material '{material.kurztext_de}' wurde durch Tabellen-Massenbearbeitung von '{request.user.email}' aktualisiert.")
                    
                    if updated_count > 0:
                        messages.success(
                            request, 
                            f"{updated_count} Material(ien) wurden erfolgreich aktualisiert."
                        )
                    else:
                        messages.info(request, "Keine Änderungen wurden vorgenommen.")
                    
                    return redirect('list_material_il')
                    
            except Exception as e:
                error_msg = f"Fehler bei der Tabellen-Massenbearbeitung: {str(e)}"
                logger.error(error_msg)
                messages.error(request, error_msg)
        else:
            # Handle form errors...
            error_count = 0
            for material_form_data in material_forms:
                form = material_form_data['form']
                material = material_form_data['material']
                
                for field_name, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Material {material.systemname} - {field_name}: {error}")
                        error_count += 1
            
            if error_count > 0:
                messages.error(request, f"Es wurden {error_count} Validierungsfehler gefunden. Bitte korrigieren Sie diese.")

        # Re-render with errors
        sample_form = MaterialForm_IL(
            editable_fields=tabular_editable_fields,  # Use the modified list
            is_mass_update=True
        )
        
        editable_fields = []
        for field in sample_form.get_normal_fields():
            if not field.is_hidden:
                editable_fields.append({
                    'name': field.name,
                    'label': field.label,
                    'required': field.name in sample_form.get_required_field_names(),
                    'help_text': field.help_text
                })

        context = {
            'material_forms': material_forms,
            'materials': materials,
            'material_count': materials.count(),
            'editable_fields': editable_fields,
        }
        return render(request, self.template_name, context)

class TabularFieldsMassUpdateMaterial_LBA_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    template_name = 'lba/tabular_fields_update_material_lba.html'
    success_url = reverse_lazy('list_material_lba')
    success_message = "Die Materialien wurden erfolgreich aktualisiert."
    allowed_groups = ['grLBA']


class TabularFieldsMassUpdateMaterial_IL_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    template_name = 'il/tabular_fields_mass_update_material_il.html'
    success_url = reverse_lazy('list_material_il')
    success_message = "Die Materialien wurden erfolgreich aktualisiert."
    allowed_groups = ['grIL']

    def get(self, request, *args, **kwargs):
        material_ids = request.GET.getlist('materials')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Felder-Tabellen-Massenbearbeitung ausgewählt.")
            return redirect('list_material_il')

        materials = Material.objects.filter(id__in=material_ids).order_by('positions_nr')
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_il')

        # Create a modified field list
        tabular_editable_fields = [field for field in EDITABLE_FIELDS_IL_TABULAR_MASS_UPDATE if field != 'systemname']

        # Create a form for each material to get field information
        sample_form = MaterialForm_IL(
            editable_fields=tabular_editable_fields,
            is_mass_update=True
        )
        
        # Get field information for the table rows
        editable_fields = []
        for field in sample_form.get_normal_fields():
            if not field.is_hidden:
                editable_fields.append({
                    'name': field.name,
                    'label': field.label,
                    'required': field.name in sample_form.get_required_field_names(),
                    'help_text': field.help_text,
                    'field_type': field.field.__class__.__name__,
                    'widget_type': field.field.widget.__class__.__name__
                })

        # Get current values for each material and field
        material_field_data = []
        for material in materials:
            material_data = {
                'material': material,
                'field_values': {}
            }
            
            for field_info in editable_fields:
                field_name = field_info['name']
                value = getattr(material, field_name, None)
                
                # Handle foreign key fields
                if hasattr(sample_form.fields.get(field_name, None), 'queryset'):
                    if value:
                        material_data['field_values'][field_name] = value.idx if hasattr(value, 'idx') else value
                    else:
                        material_data['field_values'][field_name] = ''
                else:
                    material_data['field_values'][field_name] = value if value is not None else ''
            
            material_field_data.append(material_data)

        context = {
            'materials': materials,
            'material_count': materials.count(),
            'editable_fields': editable_fields,
            'material_field_data': material_field_data,
            'sample_form': sample_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        material_ids = request.POST.getlist('material_ids')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Felder-Tabellen-Massenbearbeitung ausgewählt.")
            return redirect('list_material_il')

        materials = Material.objects.filter(id__in=material_ids).order_by('positions_nr')
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_il')

        # Use the same filtered field list
        tabular_editable_fields = [field for field in EDITABLE_FIELDS_IL_TABULAR_MASS_UPDATE if field != 'systemname']

        try:
            with transaction.atomic():
                updated_count = 0
                
                for material in materials:
                    material_updated = False
                    
                    for field_name in tabular_editable_fields:
                        # Get the field value from POST data
                        field_key = f"{field_name}_{material.id}"
                        new_value = request.POST.get(field_key)
                        
                        if new_value is not None:
                            # Get current value
                            current_value = getattr(material, field_name, None)
                            
                            # Handle different field types
                            if field_name in ['instandsetzbar', 'chargenpflicht', 'is_finished']:
                                # Boolean fields
                                new_value = new_value == 'on'
                                if current_value != new_value:
                                    setattr(material, field_name, new_value)
                                    material_updated = True
                            elif field_name in ['basismengeneinheit', 'gefahrgutkennzeichen']:
                                # Foreign key fields
                                if new_value == '':
                                    new_value = None
                                else:
                                    try:
                                        new_value = int(new_value)
                                    except (ValueError, TypeError):
                                        new_value = None
                                
                                # Compare with current foreign key value
                                current_fk_value = current_value.idx if current_value else None
                                if current_fk_value != new_value:
                                    if new_value:
                                        # Get the foreign key object
                                        if field_name == 'basismengeneinheit':
                                            fk_obj = Basismengeneinheit.objects.filter(idx=new_value).first()
                                        elif field_name == 'gefahrgutkennzeichen':
                                            fk_obj = Gefahrgutkennzeichen.objects.filter(idx=new_value).first()
                                        setattr(material, field_name, fk_obj)
                                    else:
                                        setattr(material, field_name, None)
                                    material_updated = True
                            elif field_name in ['bruttogewicht', 'nettogewicht', 'preis']:
                                # Float fields
                                try:
                                    new_value = float(new_value) if new_value else None
                                except (ValueError, TypeError):
                                    new_value = None
                                if current_value != new_value:
                                    setattr(material, field_name, new_value)
                                    material_updated = True
                            elif field_name in ['positions_nr', 'mindestbestellmenge', 'lieferzeit', 'laenge', 'breite', 'hoehe', 'preiseinheit', 'lagerfaehigkeit', 'hersteller_plz']:
                                # Integer fields
                                try:
                                    new_value = int(new_value) if new_value else None
                                except (ValueError, TypeError):
                                    new_value = None
                                if current_value != new_value:
                                    setattr(material, field_name, new_value)
                                    material_updated = True
                            else:
                                # String fields
                                new_value = new_value if new_value else None
                                if current_value != new_value:
                                    setattr(material, field_name, new_value)
                                    material_updated = True
                    
                    if material_updated:
                        material.save()
                        updated_count += 1
                        logger.info(f"Material '{material.kurztext_de}' wurde durch Felder-Tabellen-Massenbearbeitung von '{request.user.email}' aktualisiert.")
                
                if updated_count > 0:
                    messages.success(
                        request, 
                        f"{updated_count} Material(ien) wurden erfolgreich aktualisiert."
                    )
                else:
                    messages.info(request, "Keine Änderungen wurden vorgenommen.")
                
                return redirect('list_material_il')
                
        except Exception as e:
            error_msg = f"Fehler bei der Felder-Tabellen-Massenbearbeitung: {str(e)}"
            logger.error(error_msg)
            messages.error(request, error_msg)
            return redirect('list_material_il')

class ShowMaterial_IL_View(ComputedContextMixin, GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'il/show_material_il.html'
    form_class = MaterialForm_IL
    allowed_groups = ['grLBA', 'grIL']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context    

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
        context['list_material_archived'] = sorted(list_material_gd_archived, key=lambda x: (int(x.positions_nr) if x.positions_nr is not None else float('inf'), x.kurztext_de or ''))
        context['list_material'] = sorted(list_material_gd, key=lambda x: (int(x.positions_nr) if x.positions_nr is not None else float('inf'), x.kurztext_de or ''))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
#        print("len(selected_material_ids) = ", str(len(selected_material_ids)))
        # To switch from LBA mode to RUAG mode
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                transfer_comment = request.POST.get('transfer_comment', '')
                selected_materials.update(is_transferred=False, transfer_date=timezone.now(), transfer_comment=transfer_comment, is_finished=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' (" + material.systemname + "') durch '" + request.user.email + "' dem Hersteller zur Nacharbeit übermittelt (Begründung: '" + transfer_comment + "')")
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' archiviert.")
            elif action == 'unarchive':
                selected_materials.update(is_archived=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' unarchiviert.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' gelöscht.")
                    material.delete()
            elif action == 'export_lba':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' exportiert (LBA).")
                return export_to_excel(selected_materials, 'LBA')
            elif action == 'export_ruag':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' exportiert (RUAG).")
                return export_to_excel(selected_materials, 'RUAG')

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

class UpdateMaterial_GD_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
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

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Start by validating the form data
                self.object = form.save(commit=False)

                # Get new files and comments
                files = self.request.FILES.getlist('attachment_files[]')
                comments = self.request.POST.getlist('attachment_comments[]')
                attachments_to_delete = self.request.POST.getlist('delete_attachments[]')

                # Handle deletion of existing attachments first
                if attachments_to_delete:
                    attachments = MaterialAttachment.objects.filter(
                        id__in=attachments_to_delete,
                        material=self.object
                    )
                    for attachment in attachments:
                        try:
                            # Delete from S3 first
                            attachment.file.delete(save=False)
                        except (BotoCoreError, ClientError) as e:
                            error_msg = f"Failed to delete file {attachment.file.name} from storage: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                        # If S3 deletion successful, delete from database
                        attachment.delete()

                # Create temporary list to track new attachments
                new_attachments = []

                # Process new file attachments
                for file, comment in zip(files, comments):
                    if file:
                        try:
                            attachment = MaterialAttachment(
                                material=self.object,
                                file=file,
                                comment=comment,
                                uploaded_by=self.request.user
                            )
                            # Validate the attachment
                            attachment.full_clean()

                            # Try to save file to S3 first
                            try:
                                # Note: Don't save to database yet
                                attachment.file.save(file.name, file, save=False)
                            except (BotoCoreError, ClientError) as e:
                                error_msg = f"Failed to upload file '{file.name}' to storage."
                                logger.error(error_msg)
                                form.add_error(None, error_msg)
                                return self.render_to_response(self.get_context_data(form=form))

                            new_attachments.append(attachment)

                        except ValidationError as e:
                            error_msg = f"Validation error for file {file.name}: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                # If we got here, all S3 operations were successful
                # Now save the material object
                self.object.save()

                # And save all new attachments to database
                for attachment in new_attachments:
                    attachment.save()

                # Log the successful update
                logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.email}' aktualisiert.")

                return super().form_valid(form)

        except ValidationError as e:
            # Clean up any files that might have been uploaded to S3 before the error
            for attachment in new_attachments:
                try:
                    attachment.file.delete(save=False)
                except (BotoCoreError, ClientError) as s3_error:
                    logger.error(f"Failed to clean up file {attachment.file.name} after error: {str(s3_error)}")

            form.add_error(None, str(e))
            return self.render_to_response(self.get_context_data(form=form))

        except (BotoCoreError, ClientError) as e:
            error_msg = f"Failed to upload file to storage."
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

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
        context['list_material_archived'] = sorted(list_material_smda_archived, key=lambda x: (int(x.positions_nr) if x.positions_nr is not None else float('inf'), x.kurztext_de or ''))
        context['list_material'] = sorted(list_material_smda, key=lambda x: (int(x.positions_nr) if x.positions_nr is not None else float('inf'), x.kurztext_de or ''))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        # To switch from LBA mode to RUAG mode
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                transfer_comment = request.POST.get('transfer_comment', '')
                selected_materials.update(is_transferred=False, transfer_date=timezone.now(), transfer_comment=transfer_comment, is_finished=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' (" + material.systemname + "') durch '" + request.user.email + "' dem Hersteller zur Nacharbeit übermittelt (Begründung: '" + transfer_comment + "')")
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' archiviert.")
            elif action == 'unarchive':
                selected_materials.update(is_archived=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' unarchiviert.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' gelöscht.")
                selected_materials.delete()
            elif action == 'export_lba':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' exportiert (LBA).")
                return export_to_excel(selected_materials, 'LBA')
            elif action == 'export_ruag':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' exportiert (RUAG).")
                return export_to_excel(selected_materials, 'RUAG')

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

class UpdateMaterial_SMDA_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
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

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Start by validating the form data
                self.object = form.save(commit=False)

                # Get new files and comments
                files = self.request.FILES.getlist('attachment_files[]')
                comments = self.request.POST.getlist('attachment_comments[]')
                attachments_to_delete = self.request.POST.getlist('delete_attachments[]')

                # Handle deletion of existing attachments first
                if attachments_to_delete:
                    attachments = MaterialAttachment.objects.filter(
                        id__in=attachments_to_delete,
                        material=self.object
                    )
                    for attachment in attachments:
                        try:
                            # Delete from S3 first
                            attachment.file.delete(save=False)
                        except (BotoCoreError, ClientError) as e:
                            error_msg = f"Failed to delete file {attachment.file.name} from storage: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                        # If S3 deletion successful, delete from database
                        attachment.delete()

                # Create temporary list to track new attachments
                new_attachments = []

                # Process new file attachments
                for file, comment in zip(files, comments):
                    if file:
                        try:
                            attachment = MaterialAttachment(
                                material=self.object,
                                file=file,
                                comment=comment,
                                uploaded_by=self.request.user
                            )
                            # Validate the attachment
                            attachment.full_clean()

                            # Try to save file to S3 first
                            try:
                                # Note: Don't save to database yet
                                attachment.file.save(file.name, file, save=False)
                            except (BotoCoreError, ClientError) as e:
                                error_msg = f"Failed to upload file '{file.name}' to storage."
                                logger.error(error_msg)
                                form.add_error(None, error_msg)
                                return self.render_to_response(self.get_context_data(form=form))

                            new_attachments.append(attachment)

                        except ValidationError as e:
                            error_msg = f"Validation error for file {file.name}: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                # If we got here, all S3 operations were successful
                # Now save the material object
                self.object.save()

                # And save all new attachments to database
                for attachment in new_attachments:
                    attachment.save()

                # Log the successful update
                logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.email}' aktualisiert.")

                return super().form_valid(form)

        except ValidationError as e:
            # Clean up any files that might have been uploaded to S3 before the error
            for attachment in new_attachments:
                try:
                    attachment.file.delete(save=False)
                except (BotoCoreError, ClientError) as s3_error:
                    logger.error(f"Failed to clean up file {attachment.file.name} after error: {str(s3_error)}")

            form.add_error(None, str(e))
            return self.render_to_response(self.get_context_data(form=form))

        except (BotoCoreError, ClientError) as e:
            error_msg = f"Failed to upload file to storage."
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

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

#############################
class ListMaterial_LBA_View(ComputedContextMixin, GroupRequiredMixin, ListView):
    model = Material
    template_name = 'lba/list_material_lba.html'
    allowed_groups = ['grLBA']

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
        list_material_lba_archived = Material.objects.filter(is_transferred=True, is_archived=True)
        list_material_lba = Material.objects.filter(is_transferred=True, is_archived=False)

        # Convert positions_nr to integers for sorting
        context['list_material_archived'] = sorted(list_material_lba_archived, key=lambda x: (int(x.positions_nr) if x.positions_nr is not None else float('inf'), x.kurztext_de or ''))
        context['list_material'] = sorted(list_material_lba, key=lambda x: (int(x.positions_nr) if x.positions_nr is not None else float('inf'), x.kurztext_de or ''))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
#        print("len(selected_material_ids) = ", str(len(selected_material_ids)))
        # To switch from LBA mode to RUAG mode
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                transfer_comment = request.POST.get('transfer_comment', '')
                selected_materials.update(is_transferred=False, transfer_date=timezone.now(), transfer_comment=transfer_comment, is_finished=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' (" + material.systemname + "') durch '" + request.user.email + "' dem Hersteller zur Nacharbeit übermittelt (Begründung: '" + transfer_comment + "')")
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' archiviert.")
            elif action == 'unarchive':
                selected_materials.update(is_archived=False)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' unarchiviert.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' gelöscht.")
                    material.delete()
            elif action == 'export_lba':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' exportiert (LBA).")
                return export_to_excel(selected_materials, 'LBA')
            elif action == 'export_ruag':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' exportiert (RUAG).")
                return export_to_excel(selected_materials, 'RUAG')

        return redirect(reverse('list_material_lba'))

class ListMaterialArchived_LBA_View(GroupRequiredMixin, ListView):
    model = Material
    template_name = 'lba/list_material_lba_archived.html'
    context_object_name = 'list_material_lba_archived'
    allowed_groups = ['grLBA']

    def get_queryset(self, **kwargs):
        # Call the superclass method to get the base queryset
        qs = super().get_queryset(**kwargs)
        # Filter the queryset to exclude transferred items
        qs = qs.filter(is_transferred=True, is_archived=True)
        # Cast 'positions_nr' to an IntegerField for proper numeric sorting
        qs = qs.annotate(positions_nr_int=Cast('positions_nr', IntegerField()))
        # Order by the cast integer field
        return qs.order_by('positions_nr_int')

class UpdateMaterial_LBA_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'lba/update_material_lba.html'
    form_class = MaterialForm_LBA
    success_url = reverse_lazy('list_material_lba')
    success_message = "Das Material wurde erfolgreich aktualisiert."
    allowed_groups = ['grLBA']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['editable_fields'] = EDITABLE_FIELDS_LBA
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Start by validating the form data
                self.object = form.save(commit=False)

                # Get new files and comments
                files = self.request.FILES.getlist('attachment_files[]')
                comments = self.request.POST.getlist('attachment_comments[]')
                attachments_to_delete = self.request.POST.getlist('delete_attachments[]')

                # Handle deletion of existing attachments first
                if attachments_to_delete:
                    attachments = MaterialAttachment.objects.filter(
                        id__in=attachments_to_delete,
                        material=self.object
                    )
                    for attachment in attachments:
                        try:
                            # Delete from S3 first
                            attachment.file.delete(save=False)
                        except (BotoCoreError, ClientError) as e:
                            error_msg = f"Failed to delete file {attachment.file.name} from storage: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                        # If S3 deletion successful, delete from database
                        attachment.delete()

                # Create temporary list to track new attachments
                new_attachments = []

                # Process new file attachments
                for file, comment in zip(files, comments):
                    if file:
                        try:
                            attachment = MaterialAttachment(
                                material=self.object,
                                file=file,
                                comment=comment,
                                uploaded_by=self.request.user
                            )
                            # Validate the attachment
                            attachment.full_clean()

                            # Try to save file to S3 first
                            try:
                                # Note: Don't save to database yet
                                attachment.file.save(file.name, file, save=False)
                            except (BotoCoreError, ClientError) as e:
                                error_msg = f"Failed to upload file '{file.name}' to storage."
                                logger.error(error_msg)
                                form.add_error(None, error_msg)
                                return self.render_to_response(self.get_context_data(form=form))

                            new_attachments.append(attachment)

                        except ValidationError as e:
                            error_msg = f"Validation error for file {file.name}: {str(e)}"
                            logger.error(error_msg)
                            form.add_error(None, error_msg)
                            return self.render_to_response(self.get_context_data(form=form))

                # If we got here, all S3 operations were successful
                # Now save the material object
                self.object.save()

                # And save all new attachments to database
                for attachment in new_attachments:
                    attachment.save()

                # Log the successful update
                logger.info(f"Material '{self.object.kurztext_de}' wurde durch '{self.request.user.email}' aktualisiert.")

                return super().form_valid(form)

        except ValidationError as e:
            # Clean up any files that might have been uploaded to S3 before the error
            for attachment in new_attachments:
                try:
                    attachment.file.delete(save=False)
                except (BotoCoreError, ClientError) as s3_error:
                    logger.error(f"Failed to clean up file {attachment.file.name} after error: {str(s3_error)}")

            form.add_error(None, str(e))
            return self.render_to_response(self.get_context_data(form=form))

        except (BotoCoreError, ClientError) as e:
            error_msg = f"Failed to upload file to storage."
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            form.add_error(None, error_msg)
            return self.render_to_response(self.get_context_data(form=form))

class MassUpdateMaterial_LBA_View(ComputedContextMixin, FormValidMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    template_name = 'lba/mass_update_material_lba.html'
    success_url = reverse_lazy('list_material_lba')
    success_message = "Die Materialien wurden erfolgreich aktualisiert."
    allowed_groups = ['grLBA']

    def get(self, request, *args, **kwargs):
        material_ids = request.GET.getlist('materials')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Massenbearbeitung ausgewählt.")
            return redirect('list_material_lba')
        
        materials = Material.objects.filter(id__in=material_ids)
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_lba')
        
        # Create form with editable fields configuration and mass update flag
        form = MaterialForm_LBA(
            editable_fields=EDITABLE_FIELDS_LBA,
            is_mass_update=True
        )
        
        context = {
            'form': form,
            'materials': materials,
            'material_count': materials.count(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        material_ids = request.POST.getlist('material_ids')
        if not material_ids:
            messages.error(request, "Keine Materialien für die Massenbearbeitung ausgewählt.")
            return redirect('list_material_lba')
        
        materials = Material.objects.filter(id__in=material_ids)
        if not materials.exists():
            messages.error(request, "Keine gültigen Materialien gefunden.")
            return redirect('list_material_lba')
        
        # Create form with mass update configuration
        form = MaterialForm_LBA(
            request.POST, 
            editable_fields=EDITABLE_FIELDS_LBA,
            is_mass_update=True
        )
        
        # Get which fields should be updated (those with checked checkboxes)
        fields_to_update = []
        for field_name in form.fields:
            checkbox_name = f"update_{field_name}"
            if request.POST.get(checkbox_name):
                fields_to_update.append(field_name)
        
        if not fields_to_update:
            messages.warning(request, "Keine Felder zum Aktualisieren ausgewählt.")
            context = {
                'form': form,
                'materials': materials,
                'material_count': materials.count(),
            }
            return render(request, self.template_name, context)

        # Custom validation for mass updates - only validate selected fields
        validation_errors = {}

        # Check each field that's being updated
        for field_name in fields_to_update:
            if field_name in form.fields:
                field = form.fields[field_name]
                raw_value = request.POST.get(field_name)

                # For required fields in the original Meta.required_fields, validate them
                if field_name in form.Meta.required_fields:
                    if not raw_value or (isinstance(raw_value, str) and raw_value.strip() == ''):
                        validation_errors[field_name] = ["Dieses Feld ist erforderlich."]

                # For foreign key fields, validate that the value exists
                if field_name in form.Meta.foreign_key_fields and raw_value:
                    try:
                        # Convert to int and check if it exists
                        if raw_value != '':
                            int(raw_value)
                    except (ValueError, TypeError):
                        validation_errors[field_name] = ["Ungültiger Wert ausgewählt."]

        # If there are validation errors, show them
        if validation_errors:
            for field_name, errors in validation_errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field_name].label}: {error}")

            context = {
                'form': form,
                'materials': materials,
                'material_count': materials.count(),
            }
            return render(request, self.template_name, context)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_count = 0
                    updated_fields = []
                    
                    # Build the list of field names for logging
                    for field_name in fields_to_update:
                        if field_name not in updated_fields:
                            updated_fields.append(field_name)
                    
                    # Update each material with the selected fields
                    for material in materials:
                        material_updated = False
                        for field_name in fields_to_update:
                            if field_name in form.cleaned_data:
                                new_value = form.cleaned_data[field_name]
                                
                                # Set the field value directly
                                # The form's clean() method has already converted values to proper types
                                setattr(material, field_name, new_value)
                                material_updated = True
                        
                        if material_updated:
                            material.save(update_fields=fields_to_update)
                            updated_count += 1
                            logger.info(f"Material '{material.kurztext_de}' wurde durch Massenbearbeitung von '{request.user.email}' aktualisiert. Felder: {', '.join(updated_fields)}")
                    
                    if updated_count > 0:
                        messages.success(
                            request, 
                            f"{updated_count} Material(ien) wurden erfolgreich aktualisiert. "
                            f"Geänderte Felder: {', '.join(updated_fields)}"
                        )
                    else:
                        messages.warning(request, "Keine Materialien wurden aktualisiert.")
                    
                    return redirect('list_material_lba')
                    
            except Exception as e:
                error_msg = f"Fehler bei der Massenbearbeitung: {str(e)}"
                logger.error(error_msg)
                messages.error(request, error_msg)
                
        else:
            # Form has errors - but only show errors for fields that were actually being updated
            for field_name, errors in form.errors.items():
                if field_name in fields_to_update:
                    for error in errors:
                        messages.error(request, f"{form.fields.get(field_name, {}).get('label', field_name)}: {error}")
        
        # If we get here, there were errors - redisplay the form
        context = {
            'form': form,
            'materials': materials,
            'material_count': materials.count(),
        }
        return render(request, self.template_name, context)

class ShowMaterial_LBA_View(ComputedContextMixin, GroupRequiredMixin, SuccessMessageMixin, DetailView):
    model = Material
    template_name = 'lba/show_material_lba.html'
    form_class = MaterialForm_LBA
    allowed_groups = ['grLBA']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context    

    def post(self, request, *args, **kwargs):
        return redirect('list_material_lba')

#############################

class Logging_View(GroupRequiredMixin, ListView):
    template_name = 'admin/logging.html'
    allowed_groups = ['grAdmin'] 
    paginate_by = 20  # Number of items per page

    def get(self, request, *args, **kwargs):
        # Create an instance of the date filter form
        from .forms.forms import LogDateFilterForm
        form = LogDateFilterForm(request.GET)

        # Default query with no date filters
        date_filter_sql = ""

        # Apply date filters if the form is valid
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if start_date and end_date:
                date_filter_sql = f"WHERE timestamp >= '{start_date}' AND timestamp <= '{end_date} 23:59:59'"
            elif start_date:
                date_filter_sql = f"WHERE timestamp >= '{start_date}'"
            elif end_date:
                date_filter_sql = f"WHERE timestamp <= '{end_date} 23:59:59'"

        with connection.cursor() as cursor:
            # First query: Get the number of materials
            cursor.execute("SELECT COUNT(*) FROM b11_1_material")
            nb_materials = cursor.fetchone()[0]

            # Second query: Get filtered log entries
            cursor.execute(f"SELECT * FROM b11_1_log_entries {date_filter_sql} ORDER BY timestamp DESC")
            rows = cursor.fetchall()

            # Get column names from cursor description
            columns = [col[0] for col in cursor.description]

            # Convert rows to a list of dictionaries
            log_entries = [dict(zip(columns, row)) for row in rows]
            nb_log_entries = len(log_entries)

        # Pagination
        page_number = request.GET.get('page', 1)
        paginator = Paginator(log_entries, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        # Context data to pass to the template
        context = {
            'nb_materials': nb_materials,
            'nb_log_entries': nb_log_entries,
            'log_entries': page_obj,  # This is now a Page object, not the full list
            'page_obj': page_obj,     # Django's ListView expects this name for pagination
            'form': form,
            'is_paginated': paginator.num_pages > 1,
        }
        return render(request, self.template_name, context)

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        # Debug the session at the very beginning
        print("\n" + "="*80)
        print("DEBUG: RegisterView.dispatch method called")
        print(f"Session key: {request.session.session_key}")
        print(f"verified_email in session: {request.session.get('verified_email')}")
        print(f"Full session data: {dict(request.session)}")
        print("="*80 + "\n")
        
        # Check if email is in session
        if not request.session.get('verified_email'):
            messages.error(request, "Please verify your email address first.")
            return redirect('pre_register')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Make sure we're explicitly getting the email from the session
        email = self.request.session.get('verified_email', '')
        
        print("\n" + "="*80)
        print("DEBUG: RegisterView.get_context_data method called")
        print(f"Email retrieved from session: '{email}'")
        print(f"Full context keys: {context.keys()}")
        print("="*80 + "\n")
        
        # Explicitly add it to the context
        context['email'] = email
        context['recaptcha_site_key'] = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', 'dummy_key')
        context['settings'] = settings  # Pass settings to template
        return context

    def get(self, request, *args, **kwargs):
        # Additional debug for the get method
        print("\n" + "="*80)
        print("DEBUG: RegisterView.get method called")
        print(f"verified_email in session: {request.session.get('verified_email')}")
        print("="*80 + "\n")
        
        # Call the standard get method
        return super().get(request, *args, **kwargs)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            submitted_email = form.cleaned_data['email']
            
            # Get email from session instead of form
            email = request.session.get('verified_email')
            
            user = User.objects.create(
                username=email,  # Set username to email
                email=submitted_email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_active=False
            )
    
            profile = form.save(commit=False)
            profile.user = user
            profile.email = submitted_email
            profile.email = email  # Also set email in profile
            profile.registration_token = get_random_string(50)
            profile.token_expiry = timezone.now() + timedelta(days=2)
            profile.status = 'pending'  # Set initial status
            profile.save()
            
            # Clear verification data from session
            if 'email_verification' in request.session:
                del request.session['email_verification']
            if 'verified_email' in request.session:
                del request.session['verified_email']
            request.session.modified = True
    
            messages.success(request, 'Registration submitted successfully! Please wait for administrator approval.')
            logger.info(f"New user registration pending approval: {submitted_email}")
            return redirect('login_user')
    
        return render(request, self.template_name, {'form': form, 'email': request.session.get('verified_email')})

class CompleteRegistrationView(FormView):
    template_name = 'admin/password_change.html'
    form_class = RegistrationPasswordForm
    success_url = reverse_lazy('login_user')

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            self.profile = Profile.objects.get(
                registration_token=token,
                token_expiry__gt=timezone.now(),
                user__is_active=False
            )
            # Store the user in the view instance
            self.user = self.profile.user
            return super().dispatch(request, *args, **kwargs)
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid or expired registration link.')
            return redirect('login_user')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the user to the form
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        # Set the new password
        self.user.set_password(form.cleaned_data['new_password1'])
        self.user.is_active = True
        self.user.save()

        # Update the profile
        self.profile.registration_token = None
        self.profile.token_expiry = None
        self.profile.save()

        messages.success(self.request, 'Registration completed! You can now login.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Display form errors as messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)

class PendingRegistrationsView(grAdmin_GroupRequiredMixin, ListView):
    model = Profile
    template_name = 'admin/pending_registrations.html'
    context_object_name = 'pending_profiles'
    allowed_groups = ['grAdmin']

    def get_queryset(self):
        return Profile.objects.filter(status='pending').order_by('-registration_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all groups starting with 'gr'
        context['groups'] = Group.objects.filter(name__startswith='gr').order_by('name')
        return context

class ApproveRegistrationView(grAdmin_GroupRequiredMixin, View):
    allowed_groups = ['grAdmin']

    def post(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id, status='pending')
            user = profile.user

            # Approve the user
            profile.status = 'approved'
            profile.save()

            # Get the selected group ID from the form
            selected_group_id = request.POST.get('selected_group')

            # Add user to the selected group
            try:
                selected_group = Group.objects.get(id=selected_group_id)
                user.groups.add(selected_group)
                logger.info(f"User {profile.email} has been assigned to group '{selected_group.name}'")
            except Group.DoesNotExist:
                logger.error(f"Group with ID {selected_group_id} not found when approving user {profile.email}")
                messages.warning(request, f"Could not assign group to {profile.email}. Please check group permissions manually.")

            # Send approval email
            registration_link = request.build_absolute_uri(
                reverse('complete_registration', args=[profile.registration_token])
            )

            email_context = {
                'email': profile.email,
                'registration_link': registration_link,
                'expiry_date': profile.token_expiry,
                'group_name': selected_group.name if 'selected_group' in locals() else 'Unknown'
            }

            email_body = render_to_string('registration/email/registration_approved_email.html', email_context)

            # Send email code
#            send_mail(
#                'Your registration has been approved',
#                email_body,
#                settings.DEFAULT_FROM_EMAIL,
#                [profile.email],
#                fail_silently=False,
#            )

            # Debug logging for the email body
            logger.info(email_body)
            messages.success(request, f'Registration for {profile.email} has been approved and assigned to {selected_group.name}.')
            logger.info(f"Registration approved for user: {profile.email} (Group: {selected_group.name})")

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
                'email': profile.email,
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

            messages.success(request, f'Registration for {profile.email} has been rejected.')
            logger.info(f"Registration rejected for user: {profile.email}")

        except Profile.DoesNotExist:
            messages.error(request, 'Profile not found.')

        return redirect('pending_registrations')

# Add this to your views.py

class CustomPasswordResetView(FormView):
    """
    Custom password reset view that prints email to console in development
    """
    template_name = 'admin/password_reset.html'
    form_class = forms.Form  # We'll define this inline
    success_url = reverse_lazy('password_reset_done')
    
    def get_form_class(self):
        class PasswordResetForm(forms.Form):
            email = forms.EmailField(
                label='E-Mail-Adresse',
                max_length=254,
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'style': 'width: 300px;',
                    'autocomplete': 'email'
                })
            )
            
            def clean_email(self):
                email = self.cleaned_data['email']
                # Check if user exists with this email
                if not User.objects.filter(email=email, is_active=True).exists():
                    # Don't reveal whether the email exists or not for security
                    # Just return the email - we'll handle the case in the view
                    pass
                return email
                
        return PasswordResetForm
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        try:
            user = User.objects.get(email=email, is_active=True)
            
            # Generate password reset token and uid
            current_site = get_current_site(self.request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Create the password reset link
            reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = f'http://{current_site.domain}{reset_link}'
            
            # Prepare email context
            email_context = {
                'email': user.email,
                'domain': current_site.domain,
                'site_name': current_site.name,
                'uid': uid,
                'user': user,
                'token': token,
                'protocol': 'http',
                'reset_url': reset_url,
            }
            
            # Render email templates
            subject = f'Password reset on {current_site.name}'
            email_body = f"""Someone asked for password reset for email {user.email}.

Follow the link below to reset your password:
{reset_url}

If you didn't request this password reset, please ignore this email.

This link will expire in a few hours for security reasons.
"""
            
            # In development environment - print details to console instead of sending email
            print("\n" + "="*80)
            print("DEVELOPMENT MODE: Password Reset Email")
            print("="*80)
            print(f"To: {user.email}")
            print(f"Subject: {subject}")
            print("-"*80)
            print(email_body)
            print("-"*80)
            print(f"RESET LINK: {reset_url}")
            print("="*80 + "\n")
            
            # Log the reset link for easy access
            logger.info(f"Password reset link for {user.email}: {reset_url}")
            
        except User.DoesNotExist:
            # User doesn't exist, but don't reveal this for security reasons
            # Still show success message
            print("\n" + "="*80)
            print("DEVELOPMENT MODE: Password Reset Attempt")
            print("="*80)
            print(f"Password reset requested for: {email}")
            print("No user found with this email address.")
            print("="*80 + "\n")
            
            logger.info(f"Password reset attempted for non-existent email: {email}")
        
        # Always show success message (don't reveal if email exists or not)
        messages.success(
            self.request, 
            "If an account with this email exists, we have sent you a password reset link."
        )
        
        return super().form_valid(form)
