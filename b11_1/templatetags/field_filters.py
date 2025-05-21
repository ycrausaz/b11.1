from django import template
from ..utils.editable_fields_config import *

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

@register.filter
def is_in_lba_fields(field_name):
    return field_name in EDITABLE_FIELDS_LBA
