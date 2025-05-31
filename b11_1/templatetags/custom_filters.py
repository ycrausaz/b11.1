from django import template
from django.db import models
import os

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def get_display_value(material, field_name):
    """
    Get the appropriate display value for a field, 
    handling foreign keys and other special cases
    """
    value = getattr(material, field_name, None)
    
    # Handle foreign key relationships
    if value and isinstance(value, models.Model):
        return str(value)
    
    # Handle None values
    if value is None:
        return ""
    
    return value
