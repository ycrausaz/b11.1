# b11_1/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary by key.
    Usage: {{ my_dict|get_item:key }}
    """
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    elif isinstance(dictionary, dict):
        return dictionary.get(key)
    else:
        return None

@register.filter
def truncatechars(value, arg):
    """
    Truncate a string after a certain number of characters.
    Usage: {{ my_string|truncatechars:20 }}
    """
    if not value:
        return value
    try:
        length = int(arg)
        if len(str(value)) > length:
            return str(value)[:length-3] + '...'
        return str(value)
    except (ValueError, TypeError):
        return value

@register.filter
def default(value, default_value):
    """
    If value is falsy, return default_value.
    Usage: {{ my_value|default:"N/A" }}
    """
    return value if value else default_value

@register.filter
def striptags(value):
    """
    Strip HTML tags from a string.
    Usage: {{ my_html|striptags }}
    """
    import re
    return re.sub(r'<[^>]*>', '', str(value))

@register.filter
def basename(value):
    """Extract basename from a file path."""
    import os
    return os.path.basename(str(value))
