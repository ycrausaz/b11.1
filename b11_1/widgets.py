# widgets.py
from django.forms import widgets
from django.utils.safestring import mark_safe
from .utils import readonly_field_style

class ReadOnlyForeignKeyWidget(widgets.Widget):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
            
        try:
            # Get the instance using idx field
            if hasattr(self.choices, 'model'):
                if value:
                    instance = self.choices.get(idx=value)
                    display_value = str(instance)
                else:
                    display_value = ''
            else:
                display_value = value or ''
        except Exception:
            display_value = value or ''

        # Apply readonly styling
        attrs['style'] = readonly_field_style()
        final_attrs = {
            'type': 'text',
            'name': name,
            'value': display_value,
            'readonly': 'readonly',
            'class': 'form-control'
        }
        final_attrs.update(attrs)

        # Create the HTML attributes string
        html_attrs = ''
        for key, val in final_attrs.items():
            html_attrs += f' {key}="{val}"'

        return mark_safe(f'<input{html_attrs} />')
