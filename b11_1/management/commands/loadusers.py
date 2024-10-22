import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db import transaction

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
                    # Check if the row has exactly 5 columns
                    if len(row) != 5:
                        self.stdout.write(self.style.ERROR(f'Row {row_num} has incorrect number of columns'))
                        continue

                    # Extract and strip data from the row
                    email, first_name, last_name, group_name, password = [item.strip() for item in row]

                    # Validate that email, group_name, and password are provided
                    if not email or not group_name or not password:
                        self.stdout.write(self.style.ERROR(f'Row {row_num}: Email, group, and password are required'))
                        continue

                    try:
                        # Create or update the user
                        user, created = User.objects.get_or_create(username=email)
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name

                        # Set the user's password from the CSV
                        user.set_password(password)
                        user.save()

                        # Get or create the group; assumes groups are pre-defined
                        group, _ = Group.objects.get_or_create(name=group_name)
                        # Add the user to the group
                        user.groups.add(group)

                        action = 'Created' if created else 'Updated'
                        self.stdout.write(self.style.SUCCESS(f'{action} user {email} and added to group {group_name}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Row {row_num}: Error processing user {email} - {e}'))

        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
