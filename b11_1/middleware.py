import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

class EnsureProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            Profile.objects.get_or_create(user=request.user)

