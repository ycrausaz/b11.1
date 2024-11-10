# widgets.py
from django.forms import widgets
from django.utils.safestring import mark_safe
from .utils import readonly_field_style

class ReadOnlyForeignKeyWidget(widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        if value is None:
            return ''
        foreign_key_instance = self.choices.queryset.get(idx=value)
        attrs['style'] = readonly_field_style()
        rendered_html = '<input type="text" value="%s" readonly style="%s"/>' % (foreign_key_instance.__str__(), attrs['style'])
        return mark_safe(rendered_html)

