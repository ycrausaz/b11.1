# widgets.py
from django.forms import widgets
from django.utils.safestring import mark_safe
from .utils import readonly_field_style

class ReadOnlyForeignKeyWidget(widgets.Widget):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = choices

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        return value

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        if value is None:
            return ''

        # Get the related model
        model = self.choices.queryset.model if hasattr(self.choices, 'queryset') else None
        if model is None:
            return ''

        try:
            # Try to get the instance using the foreign key relationship
            if hasattr(model, 'idx'):
                instance = model.objects.get(idx=value)
            else:
                instance = model.objects.get(pk=value)
            
            display_value = str(instance)
        except (model.DoesNotExist, AttributeError, ValueError):
            display_value = ''

        attrs['style'] = readonly_field_style()
        final_attrs = self.build_attrs(attrs, {'type': 'text', 'name': name, 'value': display_value, 'readonly': 'readonly'})
        return mark_safe('<input%s />' % widgets.flatatt(final_attrs))
