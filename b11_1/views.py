# views.py

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Material, Zuteilung, Auspraegung, G_Partner, MaterialAttachment, MAX_ATTACHMENTS_PER_MATERIAL, MAX_ATTACHMENT_SIZE
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
from .forms import EmailVerificationForm
from .forms import RegistrationPasswordForm
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
from django.db import transaction
from django.core.exceptions import ValidationError
from botocore.exceptions import BotoCoreError, ClientError
from .log_export_utils import export_logs_to_excel
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

#class RegisterView(FormView):
#    """
#    Main registration form view
#    """
#    template_name = 'registration/register.html'
#    form_class = UserRegistrationForm
#
#    # In RegisterView class, add this method:
#    def get(self, request, *args, **kwargs):
#        # Debug the session data when rendering the form
#        print("\n" + "="*80)
#        print("DEBUG: RegisterView.get method called")
#        print(f"Session key: {request.session.session_key}")
#        print(f"verified_email in session: {request.session.get('verified_email')}")
#        print(f"Full session data: {dict(request.session)}")
#        print("="*80 + "\n")
#        
#        form = self.get_form()
#        return self.render_to_response(self.get_context_data(form=form))
#
#    def dispatch(self, request, *args, **kwargs):
#        # Check if email is in session
#        if not request.session.get('verified_email'):
#            messages.error(request, "Please verify your email address first.")
#            return redirect('pre_register')
#        return super().dispatch(request, *args, **kwargs)
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        
#        # Try getting from session first
#        email_from_session = self.request.session.get('verified_email')
#        
#        # If not in session, check if it might be in GET params (as fallback)
#        email_from_url = self.request.GET.get('verified_email')
#        
#        # Debug information
#        print("\n" + "="*80)
#        print(f"Email from session: {email_from_session}")
#        print(f"Email from URL param: {email_from_url}")
#        print("="*80 + "\n")
#        
#        # Use session value if available, otherwise try URL param
#        email = email_from_session or email_from_url
#        
#        context['email'] = email
#        context['recaptcha_site_key'] = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', 'dummy_key')
#        context['settings'] = settings
#        
#        return context
#    
#    def form_valid(self, form):
#        try:
#            with transaction.atomic():
#                email = self.request.session.get('verified_email')
#                
#                # Create user (inactive until approved)
#                user = User.objects.create(
#                    username=email,  # Set username to email
#                    email=email,  # Set email to email
#                    first_name=form.cleaned_data['first_name'],
#                    last_name=form.cleaned_data['last_name'],
#                    is_active=False
#                )
#                
#                # Create profile
#                profile = form.save(commit=False)
#                profile.user = user
#                profile.email = email
#                profile.registration_token = get_random_string(50)
#                profile.token_expiry = timezone.now() + timedelta(days=2)
#                profile.status = 'pending'
#                profile.save()
#                
#                # Clear verification data from session
#                if 'email_verification' in self.request.session:
#                    del self.request.session['email_verification']
#                    
#                # Add this cleanup code here
#                if 'verified_email' in self.request.session:
#                    del self.request.session['verified_email']
#                self.request.session.modified = True
#                
#                messages.success(self.request, 'Registration submitted successfully! Please wait for administrator approval.')
#                logger.info(f"New user registration pending approval: {email}")
#                
#                return redirect('login_user')
#                
#        except Exception as e:
#            logger.error(f"Error during registration: {str(e)}")
#            messages.error(self.request, f"An error occurred during registration: {str(e)}")
#            return self.form_invalid(form)

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
                    return redirect('list_material_gd')
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

        print("len(list_material_il_transferred) = ", len(list_material_il_transferred))
        print("len(list_material_il_returned) = ", len(list_material_il_returned))
        print("len(list_material_il) = ", len(list_material_il))

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
                selected_materials.update(is_transferred=True, transfer_date=timezone.now())
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' übermittelt.")
            elif action == 'delete':
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' gelöscht.")
                selected_materials.delete()
            elif action == 'archive':
                selected_materials.update(is_archived=True)
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' archiviert.")

        return redirect(reverse('list_material_il'))

class AddMaterial_IL_View(FormValidMixin_IL, GroupRequiredMixin, SuccessMessageMixin, CreateView):
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

class UpdateMaterial_IL_View(FormValidMixin_IL, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
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
        context['list_material_archived'] = sorted(list_material_gd_archived, key=lambda x: int(x.positions_nr))
        context['list_material'] = sorted(list_material_gd, key=lambda x: int(x.id))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        print("len(selected_material_ids) = ", str(len(selected_material_ids)))
        # To switch from LBA mode to RUAG mode
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                transfer_comment = request.POST.get('transfer_comment', '')
                selected_materials.update(is_transferred=False, transfer_date=timezone.now(), transfer_comment=transfer_comment)
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
        context['list_material_archived'] = sorted(list_material_smda_archived, key=lambda x: int(x.positions_nr))
        context['list_material'] = sorted(list_material_smda, key=lambda x: int(x.id))
        return context

    def post(self, request, *args, **kwargs):
        selected_material_ids = request.POST.getlist('selected_materials')
        # To switch from LBA mode to RUAG mode
        action = request.POST.get('action')

        if selected_material_ids and action:
            selected_materials = Material.objects.filter(id__in=selected_material_ids)
            if action == 'transfer':
                selected_materials.update(is_transferred=False, transfer_date=timezone.now())
                for material in selected_materials:
                    logger.info("Material '" + material.kurztext_de + "' durch '" + request.user.email + "' übermittelt.")
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

class Logging_View(GroupRequiredMixin, ListView):
    template_name = 'admin/logging.html'
    allowed_groups = ['grAdmin'] 
    paginate_by = 20  # Number of items per page

    def get(self, request, *args, **kwargs):
        # Create an instance of the date filter form
        from .forms import LogDateFilterForm
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

class ApproveRegistrationView(grAdmin_GroupRequiredMixin, View):
    allowed_groups = ['grAdmin']

    def post(self, request, profile_id):
        print("post()")
        try:
            profile = Profile.objects.get(id=profile_id, status='pending')
            print("profile = ", str(profile))
            user = profile.user

            # Approve the user
            profile.status = 'approved'
            profile.save()

            # Add user to grIL group
            try:
                il_group = Group.objects.get(name='grIL')
                user.groups.add(il_group)
            except Group.DoesNotExist:
                logger.error(f"Group 'grIL' not found when approving user {profile.email}")

            # Send approval email
            registration_link = request.build_absolute_uri(
                reverse('complete_registration', args=[profile.registration_token])
            )

            email_context = {
                'email': profile.email,
                'registration_link': registration_link,
                'expiry_date': profile.token_expiry,
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
            logger.info(email_body)
            messages.success(request, f'Registration for {profile.email} has been approved.')
            logger.info(f"Registration approved for user: {profile.email}")

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
