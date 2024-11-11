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

    class Meta(BaseTemplateForm.Meta):
        model = Material
        fields = EDITABLE_FIELDS
        required_fields = [
            'werkzuordnung_1',
            'allgemeine_positionstypengruppe',
            'spare_part_class_code',
            'materialeinstufung_nach_zuva',
            'bewertungsklasse',
        ]

    def __init__(self, *args, **kwargs):
        kwargs['editable_fields'] = EDITABLE_FIELDS_SMDA
        super().__init__(*args, **kwargs)

        # Set up foreign key fields with their querysets and required status
        foreign_key_fields = {
            'werkzuordnung_1': {'model': Werkzuordnung_1, 'queryset': Werkzuordnung_1.objects.all()},
            'allgemeine_positionstypengruppe': {'model': AllgemeinePositionstypengruppe, 'queryset': AllgemeinePositionstypengruppe.objects.all()},
            'spare_part_class_code': {'model': SparePartClassCode, 'queryset': SparePartClassCode.objects.all()},
            'materialeinstufung_nach_zuva': {'model': MaterialeinstufungNachZUVA, 'queryset': MaterialeinstufungNachZUVA.objects.all()},
            'bewertungsklasse': {'model': Bewertungsklasse, 'queryset': Bewertungsklasse.objects.all()},
        }

        # Initialize foreign key widgets and set required fields
        instance = kwargs.get('instance')

        for field_name, field_info in foreign_key_fields.items():
            if field_name in self.fields:
                queryset = field_info['queryset']

                if field_name in EDITABLE_FIELDS_SMDA:
                    # For editable fields, use Select widget with idx values
                    choices = [('', '---------')] + [(obj.idx, str(obj)) for obj in queryset]
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

                # Set required status based on Meta.required_fields
                if field_name in self.Meta.required_fields:
                    self.fields[field_name].required = True

        tooltips = HelpTooltip.objects.all()
        for field_name, field in self.fields.items():
            tooltip = tooltips.filter(field_name=field_name).first()
            if tooltip:
                field.help_text = tooltip.content
