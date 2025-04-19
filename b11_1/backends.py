from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if this is an admin login attempt
        if request and request.path.startswith('/main_admin/'):
            # For admin, use the default behavior (username)
            return super().authenticate(request, username, password, **kwargs)
        
        try:
            # For app login, use email
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class UsernameBackend(ModelBackend):
    """Standard ModelBackend for username authentication (used by admin)"""
    pass
