from django import forms
from django.forms import ModelForm
from .models import Material
from django.contrib.admin import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db import connection
from django.urls import reverse_lazy
from django.forms import DateField
from django.conf import settings
from .models import *
from .widgets import ReadOnlyForeignKeyWidget
from .utils import readonly_field_style
from .forms import CustomBooleanChoiceField, SplitterReadOnlyReadWriteFields, BaseTemplateForm
from .editable_fields_config import *

class MaterialForm_IL(BaseTemplateForm, SplitterReadOnlyReadWriteFields):

    gewichtseinheit = forms.CharField(
        label='Gewichtseinheit',
        required=False,
        disabled=True  # This marks it as disabled for BaseTemplateForm
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

#    is_finished = forms.BooleanField(
#        label='Fertig',
#        required=False,
#    )

    class Meta(BaseTemplateForm.Meta):
        model = Material
        fields = EDITABLE_FIELDS_IL
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
#            'gewichtseinheit',
            'herstellerteilenummer',
            'instandsetzbar',
            'chargenpflicht',
            'lieferzeit',
            'laenge',
            'breite',
            'hoehe',
            'preis',
#            'waehrung',
#            'cage_code',
#            'preiseinheit',
#            'hersteller_name',
#            'hersteller_adresse',
#            'hersteller_plz',
#            'hersteller_ort',
        ]
        computed_fields = [
            'gewichtseinheit',
            'waehrung',
            'einheit_l_b_h',
            'nsn_gruppe_klasse',
            'nato_versorgungs_nr',
        ]

        # Set up foreign key fields with their querysets and required status
        foreign_key_fields = {
            'basismengeneinheit': {'model': Basismengeneinheit, 'queryset': Basismengeneinheit.objects.all()},
            'gefahrgutkennzeichen': {'model': Gefahrgutkennzeichen, 'queryset': Gefahrgutkennzeichen.objects.all()},
        }

    def clean(self):
        cleaned_data = super().clean()
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
        kwargs['editable_fields'] = EDITABLE_FIELDS_IL
        super().__init__(*args, **kwargs)

        # Set required fields based on Meta.required_fields
        for field_name in self.Meta.required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        # Initialize the conditional fields as not required
        # since we'll handle validation in clean() method
        self.fields['cage_code'].required = False
        self.fields['hersteller_name'].required = False
        self.fields['hersteller_adresse'].required = False
        self.fields['hersteller_plz'].required = False
        self.fields['hersteller_ort'].required = False

        # Mark computed fields
        for field_name in self.Meta.computed_fields:
            self.fields[field_name].is_computed = True

        # Initialize foreign key widgets and set required fields
        instance = kwargs.get('instance')

        if instance:
            # Set initial values for readonly fields
            self.fields['gewichtseinheit'].initial = instance.gewichtseinheit
            self.fields['waehrung'].initial = instance.waehrung

        for field_name, field_info in self.Meta.foreign_key_fields.items():
            if field_name in self.fields:
                queryset = field_info['queryset']

                if field_name in EDITABLE_FIELDS_IL:
                    # For editable fields, use Select widget with both text and explanation
                    choices = [('', '---')]
                    for obj in queryset:
                        display_text = str(obj)  # This will use the updated __str__ method
                        choices.append((obj.idx, display_text))
                    
                    self.fields[field_name].widget = forms.Select(
                        choices=choices,
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

        # Add tooltips
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
