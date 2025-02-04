from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from symm.models import Profile

class Command(BaseCommand):
    help = 'Creates user profiles for users without one'

    def handle(self, *args, **options):
        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created user profiles'))
