from django import template
from ..editable_fields_config import EDITABLE_FIELDS_IL, EDITABLE_FIELDS_SMDA, EDITABLE_FIELDS_GD

register = template.Library()

@register.filter
def is_in_il_fields(field_name):
    return field_name in EDITABLE_FIELDS_IL

@register.filter
def is_in_smda_fields(field_name):
    return field_name in EDITABLE_FIELDS_SMDA

@register.filter
def is_in_gd_fields(field_name):
    return field_name in EDITABLE_FIELDS_GD
