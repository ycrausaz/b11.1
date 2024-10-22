import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db import transaction
from b11_1.models import Profile

class Command(BaseCommand):
    help = 'Load users from a CSV file and add them to the database'

    def add_arguments(self, parser):
        # Adds an argument for the CSV file path
        parser.add_argument('csv_file', type=str, help='The CSV file containing user data')

    @transaction.atomic  # Ensures all database operations are atomic
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Attempt to open the CSV file
        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                # Specify the delimiter as ';'
                reader = csv.reader(csvfile, delimiter=';')
                # Iterate over each row in the CSV file
                for row_num, row in enumerate(reader, start=1):
                    # Check if the row has exactly 4 columns
                    if len(row) != 4:
                        self.stdout.write(self.style.ERROR(f'Row {row_num} has incorrect number of columns'))
                        continue

                    # Extract and strip data from the row
                    email, first_name, last_name, group_name = [item.strip() for item in row]

                    # Validate that email and group_name are provided
                    if not email or not group_name:
                        self.stdout.write(self.style.ERROR(f'Row {row_num}: Email and group are required'))
                        continue

                    try:
                        # Create or update the user
                        user, created = User.objects.get_or_create(username=email)
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name

                        # Set the initial password to email concatenated twice
                        initial_password = email + email
                        user.set_password(initial_password)
                        user.save()

                        # Update the user profile to require password change
                        user_profile, _ = Profile.objects.get_or_create(user=user)
                        user_profile.must_change_password = True
                        user_profile.save()

                        # Get the group; assumes groups are pre-defined
                        group = Group.objects.get(name=group_name)
                        # Add the user to the group
                        user.groups.add(group)

                        action = 'Created' if created else 'Updated'
                        self.stdout.write(self.style.SUCCESS(f'{action} user {email} and added to group {group_name}'))

                        # Output the initial password securely
                        self.stdout.write(self.style.WARNING(f'Initial password for {email}: {initial_password}'))

                    except Group.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Row {row_num}: Group "{group_name}" does not exist'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Row {row_num}: Error processing user {email} - {e}'))

        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

