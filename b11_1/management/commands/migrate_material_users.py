from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from b11_1.models import Material, MaterialUserAssociation

class Command(BaseCommand):
    help = 'Migrate existing material-user relationships to new association model'

    def handle(self, *args, **options):
        migrated_count = 0
        
        for material in Material.objects.all():
            if material.hersteller:
                try:
                    user = User.objects.get(email=material.hersteller)
                    association, created = MaterialUserAssociation.objects.get_or_create(
                        material=material,
                        user=user,
                        defaults={
                            'is_primary': True,
                            'assigned_by': None  # Historical data
                        }
                    )
                    if created:
                        migrated_count += 1
                        self.stdout.write(f"Migrated: {material.kurztext_de} -> {user.email}")
                
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"User not found for email: {material.hersteller}")
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully migrated {migrated_count} material-user associations")
        )
