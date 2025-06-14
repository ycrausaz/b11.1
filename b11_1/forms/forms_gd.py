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

class MaterialForm_GD(BaseTemplateForm, SplitterReadOnlyReadWriteFields):

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
        ]
        computed_fields = [
            'revision_fremd',
            'materialzustandsverwaltung',
        ]

        # Set up foreign key fields with their querysets and required status
        foreign_key_fields = {
            'basismengeneinheit': {'model': Basismengeneinheit, 'queryset': Basismengeneinheit.objects.all()},
            'begru': {'model': BEGRU, 'queryset': BEGRU.objects.all()},
            'materialart_grunddaten': {'model': Materialart, 'queryset': Materialart.objects.all()},
            'sparte': {'model': Sparte, 'queryset': Sparte.objects.all()},
            'rueckfuehrungscode': {'model': Rueckfuehrungscode, 'queryset': Rueckfuehrungscode.objects.all()},
            'serialnummerprofil': {'model': Serialnummerprofil, 'queryset': Serialnummerprofil.objects.all()},
            'spare_part_class_code': {'model': SparePartClassCode, 'queryset': SparePartClassCode.objects.all()},
            'uebersetzungsstatus': {'model': Uebersetzungsstatus, 'queryset': Uebersetzungsstatus.objects.all()},
            'gefahrgutkennzeichen': {'model': Gefahrgutkennzeichen, 'queryset': Gefahrgutkennzeichen.objects.all()},
            'werkzuordnung_1': {'model': Werkzuordnung_1, 'queryset': Werkzuordnung_1.objects.all()},
            'werkzuordnung_2': {'model': Werkzuordnung_2, 'queryset': Werkzuordnung_2.objects.all()},
            'werkzuordnung_3': {'model': Werkzuordnung_3, 'queryset': Werkzuordnung_3.objects.all()},
            'werkzuordnung_4': {'model': Werkzuordnung_4, 'queryset': Werkzuordnung_4.objects.all()},
            'allgemeine_positionstypengruppe': {'model': AllgemeinePositionstypengruppe, 'queryset': AllgemeinePositionstypengruppe.objects.all()},
            'fertigungssteuerer': {'model': Fertigungssteuerer, 'queryset': Fertigungssteuerer.objects.all()},
            'sonderablauf': {'model': Sonderablauf, 'queryset': Sonderablauf.objects.all()},
            'temperaturbedingung': {'model': Temperaturbedingung, 'queryset': Temperaturbedingung.objects.all()},
            'bewertungsklasse': {'model': Bewertungsklasse, 'queryset': Bewertungsklasse.objects.all()},
            'materialeinstufung_nach_zuva': {'model': MaterialeinstufungNachZUVA, 'queryset': MaterialeinstufungNachZUVA.objects.all()},
            'zuteilung': {'model': Zuteilung, 'queryset': Zuteilung.objects.all()},
            'auspraegung': {'model': Auspraegung, 'queryset': Auspraegung.objects.all()},
        }

    def __init__(self, *args, **kwargs):
        kwargs['editable_fields'] = EDITABLE_FIELDS_GD
        super().__init__(*args, **kwargs)

        # Set required fields based on Meta.required_fields
        for field_name in self.Meta.required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        # Mark computed fields
        for field_name in self.Meta.computed_fields:
            self.fields[field_name].is_computed = True

        # Initialize foreign key widgets and set required fields
        instance = kwargs.get('instance')

        if instance:
            # Set initial values for readonly fields
            self.fields['revision_fremd'].initial = instance.revision_fremd
            self.fields['materialzustandsverwaltung'].initial = instance.materialzustandsverwaltung

        for field_name, field_info in self.Meta.foreign_key_fields.items():
            if field_name in self.fields:
                queryset = field_info['queryset']

                if field_name in EDITABLE_FIELDS_GD:
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
