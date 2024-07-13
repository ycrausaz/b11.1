from django import forms
from .widgets import ReadOnlyForeignKeyWidget
from .utils import readonly_field_style

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
