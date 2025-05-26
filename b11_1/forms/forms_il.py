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
        fields = EDITABLE_FIELDS_IL  # Make sure this doesn't include 'hersteller'
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

    def clean(self):
        cleaned_data = super().clean()
        cage_code = cleaned_data.get('cage_code')
        hersteller_name = cleaned_data.get('hersteller_name')
        hersteller_adresse = cleaned_data.get('hersteller_adresse')
        hersteller_plz = cleaned_data.get('hersteller_plz')
        hersteller_ort = cleaned_data.get('hersteller_ort')
        
        # Validation logic remains the same for manufacturer details vs CAGE code
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
        
        elif not all([hersteller_name, hersteller_adresse, hersteller_plz, hersteller_ort]):
            if not cage_code:
                self.add_error('cage_code', "CAGE Code ist erforderlich, wenn Herstellerinformationen nicht vollständig sind.")
                
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs['editable_fields'] = EDITABLE_FIELDS_IL
        super().__init__(*args, **kwargs)

        # Set required fields
        for field_name in self.Meta.required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        # Initialize conditional fields as not required
        self.fields['cage_code'].required = False
        self.fields['hersteller_name'].required = False
        self.fields['hersteller_adresse'].required = False
        self.fields['hersteller_plz'].required = False
        self.fields['hersteller_ort'].required = False

        # Mark computed fields
        for field_name in self.Meta.computed_fields:
            self.fields[field_name].is_computed = True

        # Rest of initialization remains the same...
        # (foreign key handling, tooltips, etc.)
