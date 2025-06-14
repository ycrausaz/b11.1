import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if not user.is_superuser:
        logger.info(f'User {user.email} logged in.')
        user.profile.failed_login_attempts = 0
        user.profile.save()

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if not user.is_superuser:
        logger.info(f'User {user.email} logged out.')

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    email = credentials.get('email')
    try:
        user = User.objects.get(email=email)
        if not user.is_superuser:
            logger.warning(f'Login failed for user: {email}')
    except User.DoesNotExist:
        # If user doesn't exist, log it anyway as it could be a security concern
        logger.warning(f'Login failed for user: {email}')
