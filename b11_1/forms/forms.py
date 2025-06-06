from django import forms
from ..utils.widgets import ReadOnlyForeignKeyWidget
from ..utils.utils import readonly_field_style
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import SetPasswordForm
from ..models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
import logging

logger = logging.getLogger(__name__)

# In forms.py - Update the widget IDs
class RegistrationPasswordForm(forms.Form):
    """Form for setting password during registration"""
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password1'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password2'}),
        strip=False,
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # This ensures the individual field cleaners are called
        if 'new_password1' in cleaned_data:
            self.clean_new_password1()
        if 'new_password2' in cleaned_data:
            self.clean_new_password2()

        return cleaned_data

    def clean_new_password1(self):
#        print("clean_new_password1 called")  # Debug message
        password = self.cleaned_data.get('new_password1')

        errors = []

        # Validation rules
        if len(password) < 8:
            errors.append(_("Password must be at least 8 characters long."))

        if not any(char.isupper() for char in password):
            errors.append(_("Password must contain at least one uppercase letter."))

        if not any(char.islower() for char in password):
            errors.append(_("Password must contain at least one lowercase letter."))

        # Raise all errors if any
        if errors:
            for error in errors:
                print(f"Validation error: {error}")  # Debug message
            raise ValidationError(errors)

        return password

    def clean_new_password2(self):
#        print("clean_new_password2")
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("The two password fields didn't match."))
        return password2

class CustomPasswordResetForm(SetPasswordForm):
    """
    Custom form for resetting passwords with enhanced validation
    """
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        # Password needs to have at least 8 characters
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        
        # Password needs to have at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError(_("Password must contain at least one uppercase letter."))
        
        # Password needs to have at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError(_("Password must contain at least one lowercase letter."))
        
        # Password needs to have at least one digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Password must contain at least one digit."))
        
        # Password needs to have at least one special character
        special_characters = r"[~!@#$%^&*()_+{}\":;'[\]]"
        if not bool(re.search(special_characters, password)):
            raise ValidationError(_("Password must contain at least one special character (~!@#$%^&*()_+{}\":;'[])."))
        
        return password

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom form for changing password
    """
    pass

class EmailVerificationForm(forms.Form):
    """
    Form for initial email verification step
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    recaptcha_token = forms.CharField(required=False, widget=forms.HiddenInput())
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email already exists in User model
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        
        return email
    
    def clean_recaptcha_token(self):
        token = self.cleaned_data.get('recaptcha_token', '')
        
        # If we're in development mode, bypass reCAPTCHA verification
        if getattr(settings, 'BYPASS_RECAPTCHA', False):
            logger.debug("DEVELOPMENT MODE: Bypassing reCAPTCHA verification")
            return token
        
        # Verify reCAPTCHA
        self.verify_recaptcha(token)
        return token
    
    def verify_recaptcha(self, token):
        # Skip verification in development mode
        if getattr(settings, 'BYPASS_RECAPTCHA', False):
            return
            
        # Verify reCAPTCHA with Google's API
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()
        
        if not result.get('success', False):
            raise ValidationError(_("reCAPTCHA verification failed. Please try again."))
        
        # Check the score
        score = result.get('score', 0)
        if score < settings.RECAPTCHA_REQUIRED_SCORE:
            raise ValidationError(_("reCAPTCHA score too low. Please try again."))

class CustomBooleanChoiceField(forms.TypedChoiceField):
    BOOLEAN_CHOICES = (
        (None, '---'),
        (True, 'Yes'),
        (False, 'No'),
    )

    def __init__(self, required=False, default=None, *args, **kwargs):
        kwargs['initial'] = default
        super().__init__(
            choices=self.BOOLEAN_CHOICES,
            coerce=lambda x: x == 'True',
            required=required,
            empty_value=None,
            *args,
            **kwargs
        )

    def validate(self, value):
        if self.required and (value in self.empty_values or value is None):
            raise forms.ValidationError(self.error_messages['required'], code='required')
        super().validate(value)

class SplitterReadOnlyReadWriteFields(forms.Form):
    def get_readonly_fields(self):
        for field in self:
            if field.field.widget.attrs.get('readonly', False):
                yield field

    def get_normal_fields(self):
        for field in self:
            if not field.field.widget.attrs.get('readonly', False):
                yield field

class BaseTemplateForm(forms.ModelForm):
    """
    Base form to handle readonly and editable fields.
    """
    class Meta:
        model = Material
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        editable_fields = kwargs.pop('editable_fields', None)
        super().__init__(*args, **kwargs)

        if editable_fields:
            # Get computed fields from the specific form's Meta class before removing fields
            computed_fields = getattr(self.Meta, 'computed_fields', [])

            # Import IL fields to determine what should be readonly
            from ..utils.editable_fields_config import EDITABLE_FIELDS_IL

            # Get all model fields
            all_fields = [field.name for field in self._meta.model._meta.fields]

            # Instead of removing fields, categorize them
            fields_to_remove = []
            fields_to_make_readonly = []

            for field_name in self.fields:
                if field_name not in editable_fields and field_name not in computed_fields:
                    # Check if it's an IL field that should be shown as readonly
                    if field_name in EDITABLE_FIELDS_IL:
                        fields_to_make_readonly.append(field_name)
                    else:
                        # Remove fields that are neither editable nor IL fields
                        fields_to_remove.append(field_name)

            # Actually remove the fields that shouldn't be shown at all
            for field_name in fields_to_remove:
                del self.fields[field_name]

            # For remaining fields, set readonly/disabled status
            for field_name in self.fields:
                field = self.fields[field_name]

                if field_name in fields_to_make_readonly:
                    # IL fields in LBA forms should be readonly
                    field.disabled = True
                    field.widget.attrs['readonly'] = True
                    field.is_readonly_il = True  # Mark as IL readonly field
                elif field_name not in editable_fields and field_name not in computed_fields:
                    # Other non-editable fields
                    field.disabled = True
                    field.widget.attrs['readonly'] = True
                elif field_name in computed_fields:
                    # Mark computed fields as disabled and computed
                    field.disabled = True
                    field.widget.attrs['readonly'] = True
                    field.is_computed = True

    def get_normal_fields(self):
        """Return only editable fields."""
        return [field for field in self if not field.field.disabled and not getattr(field.field, 'is_computed', False)]

    def get_computed_fields(self):
        """Return computed fields."""
        return [field for field in self if getattr(field.field, 'is_computed', False)]

    def get_readonly_fields(self):
        """Return only readonly fields, excluding computed fields."""
        return [field for field in self if field.field.disabled and not getattr(field.field, 'is_computed', False)]

    def get_il_readonly_fields(self):
        """Return IL fields that are shown as readonly in LBA forms."""
        return [field for field in self if getattr(field.field, 'is_readonly_il', False)]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # Only update fields that exist in the form and are editable
            update_fields = [field.name for field in self.get_normal_fields() if field.name in self.fields]
            if update_fields:
                instance.save(update_fields=update_fields)
            else:
                instance.save()
        return instance

class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration
    """
    recaptcha_token = forms.CharField(required=False, widget=forms.HiddenInput())

    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    firm = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'firm', 'role', 'country', 'phone']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'firm': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("This username is already taken."))
        return username
    
    def clean_recaptcha_token(self):
        token = self.cleaned_data.get('recaptcha_token', '')
        
        # If we're in development mode, bypass reCAPTCHA verification
        if getattr(settings, 'BYPASS_RECAPTCHA', False):
            logger.debug("DEVELOPMENT MODE: Bypassing reCAPTCHA verification")
            return token
        
        # Verify reCAPTCHA
        self.verify_recaptcha(token)
        return token
    
    def verify_recaptcha(self, token):
        # Skip verification in development mode
        if getattr(settings, 'BYPASS_RECAPTCHA', False):
            return
            
        # Verify reCAPTCHA with Google's API
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()
        
        if not result.get('success', False):
            raise ValidationError(_("reCAPTCHA verification failed. Please try again."))
        
        # Check the score
        score = result.get('score', 0)
        if score < settings.RECAPTCHA_REQUIRED_SCORE:
            raise ValidationError(_("reCAPTCHA score too low. Please try again."))

class LogDateFilterForm(forms.Form):
    start_date = forms.DateField(
        label=_('Start Date'),
        required=False,
        widget=DatePickerInput(
            options={
                'format': 'DD.MM.YYYY',
                'showClose': True,
                'showClear': True,
                'showTodayButton': True,
            }
        )
    )
    end_date = forms.DateField(
        label=_('End Date'),
        required=False,
        widget=DatePickerInput(
            options={
                'format': 'DD.MM.YYYY',
                'showClose': True,
                'showClear': True,
                'showTodayButton': True,
            }
        )
    )
