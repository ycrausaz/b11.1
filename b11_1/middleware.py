import logging
from django.utils.deprecation import MiddlewareMixin
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

class EnsureProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            Profile.objects.get_or_create(user=request.user)

logger = logging.getLogger(__name__)

class UserActivityLoggingMiddleware(MiddlewareMixin):
    @receiver(user_logged_in)
    def log_user_login(sender, request, user, **kwargs):
        logger.info(f'User {user.username} logged in.')
        user.profile.failed_login_attempts = 0
        user.profile.save()

    @receiver(user_logged_out)
    def log_user_logout(sender, request, user, **kwargs):
        logger.info(f'User {user.username} logged out.')

    @receiver(user_login_failed)
    def log_user_login_failed(sender, credentials, request, **kwargs):
        username = credentials.get('username')
        logger.warning(f'Login failed for user: {username}')
        
        try:
            user = User.objects.get(username=username)
            profile = user.profile
            profile.failed_login_attempts += 1
            profile.save()

            if profile.failed_login_attempts >= 3:
                current_site = get_current_site(request)
                mail_subject = 'Reset your password'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_url = f'http://{current_site.domain}{reset_link}'
                message = f'It seems you have failed to login 3 times. Please reset your password using the following link:\n{reset_url}'
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                logger.info(f'Password reset email sent to user: {username}')

        except User.DoesNotExist:
            pass

