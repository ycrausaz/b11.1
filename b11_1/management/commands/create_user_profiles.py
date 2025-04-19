# management/commands/create_user_profiles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from b11_1.models import Profile

class Command(BaseCommand):
    help = 'Creates user profiles for users without one'

    def handle(self, *args, **options):
        created_count = 0
        error_count = 0
        
        for user in User.objects.all():
            try:
                # Try to get existing profile
                profile = Profile.objects.filter(user=user).first()
                
                if not profile:
                    # Create profile with email from user
                    email = user.email
                    if not email:
                        # If user has no email, generate a placeholder one based on id
                        email = f"user_{user.id}@placeholder.com"
                        self.stdout.write(self.style.WARNING(f'User {user} has no email, using placeholder: {email}'))
                    
                    Profile.objects.create(
                        user=user,
                        email=email,
                        first_name=user.first_name,
                        last_name=user.last_name
                    )
                    created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating profile for {user}: {str(e)}'))
                error_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} user profiles. Encountered {error_count} errors.'))
