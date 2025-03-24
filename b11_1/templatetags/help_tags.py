# b11_1/templatetags/help_tags.py
from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from ..models import HelpTooltip

register = template.Library()

@register.filter(name='add_tooltip')
def add_tooltip(field):
    """Add tooltip to field label and return label with tooltip"""
    field_name = field.name
    label = field.label
    current_language = get_language()

    try:
        help_obj = HelpTooltip.objects.filter(field_name=field_name).first()
        if help_obj:
            # Get help content in current language
            help_content = help_obj.get_help_content(current_language)
            if help_content:
                # Create the tooltip part with translated content
                tooltip_html = f'<label for="{field.id_for_label}" data-bs-toggle="tooltip" title="{help_content}">{label}</label>'
                return mark_safe(tooltip_html)
    except Exception:
        pass

    return label

@register.filter(name='get_inline_help')
def get_inline_help(field):
    """Get inline help text for a field if it exists"""
    field_name = field.name
    current_language = get_language()

    try:
        help_obj = HelpTooltip.objects.filter(field_name=field_name).first()
        if help_obj:
            # Get inline help in current language
            inline_help = help_obj.get_inline_help(current_language)
            if inline_help:
                return mark_safe(f'<div class="field-inline-help">{inline_help}</div>')
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
