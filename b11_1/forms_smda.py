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

class MaterialForm_SMDA(BaseTemplateForm, SplitterReadOnlyReadWriteFields):

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
            'werkzuordnung_1',
            'allgemeine_positionstypengruppe',
            'spare_part_class_code',
            'materialeinstufung_nach_zuva',
            'bewertungsklasse',
            'zuteilung',
            'auspraegung',
        ]
        computed_fields = [
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
        }

    def __init__(self, *args, **kwargs):
        kwargs['editable_fields'] = EDITABLE_FIELDS_SMDA
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
            self.fields['verkaufsorg'].initial = instance.verkaufsorg
            self.fields['vertriebsweg'].initial = instance.vertriebsweg
            self.fields['auszeichnungsfeld'].initial = instance.auszeichnungsfeld
            self.fields['preissteuerung'].initial = instance.preissteuerung
            self.fields['preisermittlung'].initial = instance.preisermittlung

        for field_name, field_info in self.Meta.foreign_key_fields.items():
            if field_name in self.fields:
                queryset = field_info['queryset']

                if field_name in EDITABLE_FIELDS_SMDA:
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
