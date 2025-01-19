from django import forms
from .widgets import ReadOnlyForeignKeyWidget
from .utils import readonly_field_style
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import SetPasswordForm
from .models import *

class CustomPasswordResetForm(SetPasswordForm):
    def clean_new_password2(self):
        password2 = self.cleaned_data.get('new_password2')
        user = self.user
        try:
            validate_password(password2, user)
        except forms.ValidationError as error:
            self.add_error('new_password2', error)
        return password2

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        password2 = self.cleaned_data.get('new_password2')
        user = self.user
        try:
            validate_password(password2, user)
        except forms.ValidationError as error:
            self.add_error('new_password2', error)
        return password2

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
            for field_name in self.fields:
                field = self.fields[field_name]
                if field_name not in editable_fields:
                    # If it's not in editable_fields, mark it as disabled
                    field.disabled = True
                    # Also ensure the widget has readonly attribute
                    field.widget.attrs['readonly'] = True

    def get_normal_fields(self):
        """Return only editable fields."""
        return [field for field in self if not field.field.disabled and not getattr(field.field, 'is_computed', False)]

    def get_computed_fields(self):
        """Return computed fields."""
        return [field for field in self if getattr(field.field, 'is_computed', False)]

    def get_readonly_fields(self):
        """Return only readonly fields, excluding computed fields."""
        return [field for field in self if field.field.disabled and not getattr(field.field, 'is_computed', False)]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save(update_fields=[field.name for field in self.get_normal_fields()])
        return instance
