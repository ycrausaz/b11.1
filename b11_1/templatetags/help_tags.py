# templatetags/help_tags.py
from django import template
from django.utils.safestring import mark_safe
from ..models import HelpTooltip

register = template.Library()

@register.filter(name='add_tooltip')
def add_tooltip(field):
    """Add tooltip to field label and return label with tooltip"""
    field_name = field.name
    label = field.label
    
    try:
        help_obj = HelpTooltip.objects.filter(field_name=field_name).first()
        if help_obj:
            # Create the tooltip part (keep existing functionality)
            tooltip_html = f'<label for="{field.id_for_label}" data-bs-toggle="tooltip" title="{help_obj.content}">{label}</label>'
            
            # We'll only return the tooltip part here - the inline help will be handled separately
            return mark_safe(tooltip_html)
    except Exception:
        pass
        
    return label

@register.filter(name='get_inline_help')
def get_inline_help(field):
    """Get inline help text for a field if it exists"""
    field_name = field.name
    
    try:
        help_obj = HelpTooltip.objects.filter(field_name=field_name).first()
        if help_obj and help_obj.inline_help:
            return mark_safe(f'<div class="field-inline-help">{help_obj.inline_help}</div>')
    except Exception:
        pass
    
    return ''

@register.filter(name='is_conditional_required')
def is_conditional_required(field):
    """Check if field is conditionally required (cage_code or hersteller fields)"""
    conditional_fields = [
        'cage_code', 'hersteller_name', 'hersteller_adresse', 
        'hersteller_plz', 'hersteller_ort'
    ]
    return field.name in conditional_fields
