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

class MaterialForm_LBA(BaseTemplateForm, SplitterReadOnlyReadWriteFields):

    revision_fremd = forms.CharField(
        label='Revision Fremd',
        required=False,
        disabled=True  # This marks it as disabled for BaseTemplateForm
    )
    materialzustandsverwaltung = forms.CharField(
        label='Materialzustandsverwaltung',
        required=False,
        disabled=True
    )
    verkaufsorg = forms.CharField(
        label='Verkaufsorg.',
        required=False,
        disabled=True  # This marks it as disabled for BaseTemplateForm
    )
    vertriebsweg = forms.CharField(
        label='Vertriebsweg',
        required=False,
        disabled=True
    )
    auszeichnungsfeld = forms.CharField(
        label='Auszeichnungsfeld',
        required=False,
        disabled=True
    )
    preissteuerung = forms.CharField(
        label='Preissteuerung',
        required=False,
        disabled=True
    )
    preisermittlung = forms.CharField(
        label='Preisermittlung',
        required=False,
        disabled=True
    )

    class Meta(BaseTemplateForm.Meta):
        model = Material
        fields = EDITABLE_FIELDS
        required_fields = [
            'begru',
            'sparte',
            'geschaeftspartner',
            'warengruppe',
            'uebersetzungsstatus',
            'materialart_grunddaten',
            'produkthierarchie',
            'werkzuordnung_1',
            'allgemeine_positionstypengruppe',
            'spare_part_class_code',
            'materialeinstufung_nach_zuva',
            'bewertungsklasse',
        ]
        computed_fields = [
            'revision_fremd',
            'materialzustandsverwaltung',
            'verkaufsorg',
            'vertriebsweg',
            'auszeichnungsfeld',
            'preissteuerung',
            'preisermittlung',
        ]

        # Set up foreign key fields with their querysets and required status
        foreign_key_fields = {
            'werkzuordnung_1': {'model': Werkzuordnung_1, 'queryset': Werkzuordnung_1.objects.all()},
            'allgemeine_positionstypengruppe': {'model': AllgemeinePositionstypengruppe, 'queryset': AllgemeinePositionstypengruppe.objects.all()},
            'spare_part_class_code': {'model': SparePartClassCode, 'queryset': SparePartClassCode.objects.all()},
            'materialeinstufung_nach_zuva': {'model': MaterialeinstufungNachZUVA, 'queryset': MaterialeinstufungNachZUVA.objects.all()},
            'bewertungsklasse': {'model': Bewertungsklasse, 'queryset': Bewertungsklasse.objects.all()},
            'zuteilung': {'model': Zuteilung, 'queryset': Zuteilung.objects.all()},
            'auspraegung': {'model': Auspraegung, 'queryset': Auspraegung.objects.all()},
            'basismengeneinheit': {'model': Basismengeneinheit, 'queryset': Basismengeneinheit.objects.all()},
            'begru': {'model': BEGRU, 'queryset': BEGRU.objects.all()},
            'materialart_grunddaten': {'model': Materialart, 'queryset': Materialart.objects.all()},
            'sparte': {'model': Sparte, 'queryset': Sparte.objects.all()},
            'rueckfuehrungscode': {'model': Rueckfuehrungscode, 'queryset': Rueckfuehrungscode.objects.all()},
            'serialnummerprofil': {'model': Serialnummerprofil, 'queryset': Serialnummerprofil.objects.all()},
            'uebersetzungsstatus': {'model': Uebersetzungsstatus, 'queryset': Uebersetzungsstatus.objects.all()},
            'gefahrgutkennzeichen': {'model': Gefahrgutkennzeichen, 'queryset': Gefahrgutkennzeichen.objects.all()},
            'werkzuordnung_2': {'model': Werkzuordnung_2, 'queryset': Werkzuordnung_2.objects.all()},
            'werkzuordnung_3': {'model': Werkzuordnung_3, 'queryset': Werkzuordnung_3.objects.all()},
            'werkzuordnung_4': {'model': Werkzuordnung_4, 'queryset': Werkzuordnung_4.objects.all()},
            'fertigungssteuerer': {'model': Fertigungssteuerer, 'queryset': Fertigungssteuerer.objects.all()},
            'sonderablauf': {'model': Sonderablauf, 'queryset': Sonderablauf.objects.all()},
            'temperaturbedingung': {'model': Temperaturbedingung, 'queryset': Temperaturbedingung.objects.all()},
        }

    def get_required_field_names(self):
        """Return a list of field names that are normally required for this form"""
        return self.Meta.required_fields

    def __init__(self, *args, **kwargs):
        # Extract editable_fields and is_mass_update before calling super().__init__
        editable_fields = kwargs.pop('editable_fields', EDITABLE_FIELDS_LBA)
        is_mass_update = kwargs.pop('is_mass_update', False)
        
        # Store the mass update flag
        self.is_mass_update = is_mass_update
        
        # Pass editable_fields to the parent constructor
        kwargs['editable_fields'] = editable_fields
        super().__init__(*args, **kwargs)

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

        # Mark computed fields
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
            # Set initial values for readonly fields
            if 'revision_fremd' in self.fields:
                self.fields['revision_fremd'].initial = instance.revision_fremd
            if 'materialzustandsverwaltung' in self.fields:
                self.fields['materialzustandsverwaltung'].initial = instance.materialzustandsverwaltung
            if 'verkaufsorg' in self.fields:
                self.fields['verkaufsorg'].initial = instance.verkaufsorg
            if 'vertriebsweg' in self.fields:
                self.fields['vertriebsweg'].initial = instance.vertriebsweg
            if 'auszeichnungsfeld' in self.fields:
                self.fields['auszeichnungsfeld'].initial = instance.auszeichnungsfeld
            if 'preissteuerung' in self.fields:
                self.fields['preissteuerung'].initial = instance.preissteuerung
            if 'preisermittlung' in self.fields:
                self.fields['preisermittlung'].initial = instance.preisermittlung

        for field_name, field_info in self.Meta.foreign_key_fields.items():
            if field_name in self.fields:
                queryset = field_info['queryset']

                if field_name in editable_fields:
                    # For editable fields, use Select widget with both text and explanation
                    choices = [('', '---')]
                    for obj in queryset:
                        display_text = str(obj)  # This will use the updated __str__ method
                        choices.append((obj.idx, display_text))

                    self.fields[field_name].widget = forms.Select(choices=choices)

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

    def clean(self):
        """Override clean method to handle mass edit validation"""
        cleaned_data = super().clean()
        
        # For mass edit, we need to convert idx values back to model instances
        # This ensures Django's ModelForm can properly handle the foreign key fields
        for field_name, field_info in self.Meta.foreign_key_fields.items():
            if field_name in cleaned_data and cleaned_data[field_name]:
                value = cleaned_data[field_name]
                
                # If value is a string representation of an idx, convert it to the model instance
                if isinstance(value, str) and value.isdigit():
                    try:
                        related_model = field_info['model']
                        related_obj = related_model.objects.get(idx=int(value))
                        cleaned_data[field_name] = related_obj
                    except related_model.DoesNotExist:
                        # If the related object doesn't exist, set to None
                        cleaned_data[field_name] = None
                # If value is an integer idx, convert it to the model instance
                elif isinstance(value, int):
                    try:
                        related_model = field_info['model']
                        related_obj = related_model.objects.get(idx=value)
                        cleaned_data[field_name] = related_obj
                    except related_model.DoesNotExist:
                        # If the related object doesn't exist, set to None
                        cleaned_data[field_name] = None
                # If it's already a model instance, keep it as is
                # (this handles the normal case)
        
        return cleaned_data
