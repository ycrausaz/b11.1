from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_names):
    if user.is_authenticated:
        group_names_list = group_names.split(',')
        return user.groups.filter(name__in=group_names_list).exists()
    return False

@register.filter(name='get_user_group')
def get_user_group(user):
    if user.is_authenticated:
        groups = user.groups.all()
        if groups:
            # Return the name of the first group
            # You can modify this if users can belong to multiple groups
            return groups[0].name
    return ""
