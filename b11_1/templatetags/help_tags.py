from django import template
from django.utils.safestring import mark_safe
from ..models import HelpTooltip

register = template.Library()

@register.filter(name='add_tooltip')
def add_tooltip(field):
    tooltip = HelpTooltip.objects.filter(field_name=field.name).first()
    if tooltip:
        return mark_safe(f'<label for="{field.id_for_label}" data-toggle="tooltip" title="{tooltip.content}">{field.label}</label>')
    return field.label_tag()
