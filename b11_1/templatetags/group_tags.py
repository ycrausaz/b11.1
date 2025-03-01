from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_names):
    if user.is_authenticated:
        group_names_list = group_names.split(',')
        return user.groups.filter(name__in=group_names_list).exists()
    return False

