from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Check if user belongs to a specific group
    Usage: {% if user|has_group:"grAdmin" %}
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False

@register.filter(name='get_user_group')
def get_user_group(user):
    """
    Return the user's group name. For company groups, returns the company name.
    For system groups, returns the group name.
    Usage: {{ user|get_user_group }}
    """
    if not user.is_authenticated:
        return ""
    
    # List of system groups - groups that are not company-specific
    system_groups = ['grGD', 'grSMDA', 'grLBA', 'grAdmin']
    
    # Get all user groups
    user_groups = user.groups.values_list('name', flat=True)
    
    # Find the first non-system group (company group)
    company_groups = [g for g in user_groups if g not in system_groups]
    
    if company_groups:
        # Return the first company group (normally there should be only one)
        return company_groups[0]
    elif user_groups:
        # If no company group found but user has groups, return the first system group
        return user_groups[0]
    else:
        # If no groups found
        return "Keine Gruppe"
