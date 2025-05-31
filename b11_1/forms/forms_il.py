from django import forms
from django.forms import ModelForm
from ..models import Material
from django.contrib.admin import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db import connection
from django.urls import reverse_lazy
from django.forms import DateField
from django.conf import settings
from ..models import *
from ..utils.widgets import ReadOnlyForeignKeyWidget
from ..utils.utils import readonly_field_style
from .forms import CustomBooleanChoiceField, SplitterReadOnlyReadWriteFields, BaseTemplateForm
from ..utils.editable_fields_config import *

class MaterialForm_IL(BaseTemplateForm, SplitterReadOnlyReadWriteFields):
    
    # REMOVED: hersteller field completely - it's no longer needed
    
    gewichtseinheit = forms.CharField(
        label='Gewichtseinheit',
        required=False,
        disabled=True
    )
    waehrung = forms.CharField(
        label='Währung',
        required=False,
        disabled=True
    )
    einheit_l_b_h = forms.CharField(
        label='Einheit L / B / H',
        required=False,
        disabled=True
    )
    nsn_gruppe_klasse = forms.CharField(
        label='NSN Gruppe / Klasse',
        required=False,
        disabled=True
    )
    nato_versorgungs_nr = forms.CharField(
        label='Nato Versorgungs-Nr.',
        required=False,
        disabled=True
    )

    class Meta(BaseTemplateForm.Meta):
        model = Material
        fields = EDITABLE_FIELDS_IL  # This will be overridden in __init__ for mass updates
        required_fields = [
            'systemname',
            'kurztext_de',
            'kurztext_fr',
            'kurztext_en',
            'grunddatentext_de_1_zeile',
            'grunddatentext_fr_1_zeile',
            'grunddatentext_en_1_zeile',
            'basismengeneinheit',
            'bruttogewicht',
            'herstellerteilenummer',
            'instandsetzbar',
            'chargenpflicht',
            'lieferzeit',
            'laenge',
            'breite',
            'hoehe',
            'preis',
        ]
        computed_fields = [
            'gewichtseinheit',
            'waehrung',
            'einheit_l_b_h',
            'nsn_gruppe_klasse',
            'nato_versorgungs_nr',
        ]

        foreign_key_fields = {
            'basismengeneinheit': {'model': Basismengeneinheit, 'queryset': Basismengeneinheit.objects.all()},
            'gefahrgutkennzeichen': {'model': Gefahrgutkennzeichen, 'queryset': Gefahrgutkennzeichen.objects.all()},
        }

    def get_required_field_names(self):
        """Return a list of field names that are normally required for this form"""
        return self.Meta.required_fields

    def clean(self):
        cleaned_data = super().clean()
        # Only perform conditional validation if this is NOT a mass update form
        # Mass update forms should not enforce these conditional requirements
        if not getattr(self, 'is_mass_update', False):
            cage_code = cleaned_data.get('cage_code')
            hersteller_name = cleaned_data.get('hersteller_name')
            hersteller_adresse = cleaned_data.get('hersteller_adresse')
            hersteller_plz = cleaned_data.get('hersteller_plz')
            hersteller_ort = cleaned_data.get('hersteller_ort')

            # Check if cage_code is empty, then the other fields must be filled
            if not cage_code:
                hersteller_fields = {
                    'hersteller_name': hersteller_name,
                    'hersteller_adresse': hersteller_adresse,
                    'hersteller_plz': hersteller_plz,
                    'hersteller_ort': hersteller_ort
                }

                if not all(hersteller_fields.values()):
                    missing_fields = [field for field, value in hersteller_fields.items() if not value]
                    for field in missing_fields:
                        self.add_error(field, "Dieses Feld ist erforderlich, wenn CAGE Code nicht angegeben ist.")

            # Check if any of the hersteller fields are empty, then cage_code is required
            elif not all([hersteller_name, hersteller_adresse, hersteller_plz, hersteller_ort]):
                if not cage_code:
                    self.add_error('cage_code', "CAGE Code ist erforderlich, wenn Herstellerinformationen nicht vollständig sind.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        # Extract editable_fields before calling super().__init__
        editable_fields = kwargs.pop('editable_fields', EDITABLE_FIELDS_IL)
        is_mass_update = kwargs.pop('is_mass_update', False)

        # Debug: Print which fields are being used
#        print(f"DEBUG: MaterialForm_IL.__init__ called with editable_fields: {editable_fields}")
 #       print(f"DEBUG: is_mass_update: {is_mass_update}")

        # **KEY FIX**: Override the Meta.fields for mass updates
        if editable_fields != EDITABLE_FIELDS_IL:
#            print(f"DEBUG: Overriding Meta.fields from {self.Meta.fields} to {editable_fields}")
            self.Meta.fields = editable_fields

        # Store the mass update flag
        self.is_mass_update = is_mass_update

        # Pass editable_fields to the parent constructor
        kwargs['editable_fields'] = editable_fields
        super().__init__(*args, **kwargs)

        # Debug: Print which fields are in the form after super().__init__
#        print(f"DEBUG: Form fields after super().__init__: {list(self.fields.keys())}")

        # Remove excluded fields completely from the form (additional safety)
        if editable_fields != EDITABLE_FIELDS_IL:
            excluded_fields = set(EDITABLE_FIELDS_IL) - set(editable_fields)
#            print(f"DEBUG: Removing excluded fields: {excluded_fields}")
            for field_name in excluded_fields:
                if field_name in self.fields:
                    del self.fields[field_name]
#                    print(f"DEBUG: Removed field: {field_name}")

#        print(f"DEBUG: Final form fields: {list(self.fields.keys())}")

        # Set required fields based on Meta.required_fields (only for fields that exist)
        # For mass update forms, make all fields optional initially
        # They will be validated only if their update checkbox is checked
        for field_name in self.fields:
            if is_mass_update:
                # For mass update forms, make all fields optional
                self.fields[field_name].required = False
            else:
                # For regular forms, set required based on Meta.required_fields
                if field_name in self.Meta.required_fields:
                    self.fields[field_name].required = True

        # Initialize the conditional fields as not required (only if they exist)
        # since we'll handle validation in clean() method
        conditional_fields = ['cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort']
        for field_name in conditional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False

        # Mark computed fields (only for fields that exist)
        # This needs to be done AFTER BaseTemplateForm.__init__ has run
        for field_name in self.Meta.computed_fields:
            if field_name in self.fields:
                self.fields[field_name].is_computed = True
                # Also ensure computed fields are disabled and readonly
                self.fields[field_name].disabled = True
                self.fields[field_name].widget.attrs['readonly'] = True

        # Initialize foreign key widgets and set required fields
        instance = kwargs.get('instance')

        if instance:
            # Set initial values for readonly fields (only if they exist)
            if 'gewichtseinheit' in self.fields:
                self.fields['gewichtseinheit'].initial = instance.gewichtseinheit
            if 'waehrung' in self.fields:
                self.fields['waehrung'].initial = instance.waehrung

        for field_name, field_info in self.Meta.foreign_key_fields.items():
            if field_name in self.fields:  # Only process if field exists in form
                queryset = field_info['queryset']

                if field_name in editable_fields:
                    # For editable fields, use Select widget with both text and explanation
                    choices = [('', '---')]
                    for obj in queryset:
                        display_text = str(obj)  # This will use the updated __str__ method
                        choices.append((obj.idx, display_text))

                    # For tabular editing, use more compact styling
                    widget_attrs = {'class': 'form-select'}
                    if is_mass_update:
                        widget_attrs['class'] += ' form-select-sm'

                    self.fields[field_name].widget = forms.Select(
                        choices=choices,
                        attrs=widget_attrs
                    )

                    # Set initial value if instance exists
                    if instance:
                        value = getattr(instance, field_name)
                        if value:
                            self.fields[field_name].initial = value.idx
                else:
                    # For readonly fields, use custom widget
                    self.fields[field_name].widget = ReadOnlyForeignKeyWidget(choices=queryset)

                    # Set initial value if instance exists
                    if instance:
                        value = getattr(instance, field_name)
                        if value:
                            self.fields[field_name].initial = value.idx

        # Style form controls for tabular editing
        if is_mass_update:
            for field_name, field in self.fields.items():
                if isinstance(field.widget, forms.TextInput):
                    field.widget.attrs.update({'class': 'form-control form-control-sm'})
                elif isinstance(field.widget, forms.NumberInput):
                    field.widget.attrs.update({'class': 'form-control form-control-sm'})
                elif isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs.update({'class': 'form-check-input'})

        # Add tooltips (only for fields that exist)
        from django.utils.translation import get_language
        tooltips = HelpTooltip.objects.all()
        current_language = get_language()
        for field_name, field in self.fields.items():
            tooltip = tooltips.filter(field_name=field_name).first()
            if tooltip:
                # Get help content in current language
                help_content_field = f'help_content_{current_language}'
                if hasattr(tooltip, help_content_field) and getattr(tooltip, help_content_field):
                    field.help_text = getattr(tooltip, help_content_field)
                # Fallback to German
                elif hasattr(tooltip, 'help_content_de') and tooltip.help_content_de:
                    field.help_text = tooltip.help_content_de
