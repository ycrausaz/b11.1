# Create this file as b11_1/templatetags/path_filters.py

import os
from django import template

register = template.Library()

@register.filter
def basename(filepath):
    """
    Extract the basename from a file path
    Usage: {{ attachment.file.name|basename }}
    """
    if not filepath:
        return ''
    return os.path.basename(str(filepath))
