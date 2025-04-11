# b11_1/management/commands/populate_db.py

import os
import subprocess
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Check if we're in a local environment
        if self.is_local_environment():
            self.stdout.write(self.style.WARNING('Running in local environment. Database population skipped.'))
            self.stdout.write(self.style.WARNING('To populate the database, please run this command in a non-local environment.'))
            return

        self.stdout.write('Populating database...')

        # Find the SQL file relative to the current management command
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_dir = os.path.normpath(os.path.join(current_dir, '..', '..', 'pgsql'))
        sql_file_path = os.path.join(sql_dir, 'insert_all.txt')
        csv_file_path = os.path.join(sql_dir, 'help.csv')

        self.stdout.write(f"Looking for SQL file at: {sql_file_path}")
        self.stdout.write(f"Looking for CSV file at: {csv_file_path}")

        if not os.path.exists(sql_file_path):
            self.stdout.write(self.style.ERROR(f"SQL file not found at: {sql_file_path}"))
            return

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at: {csv_file_path}"))
            return

        with open(sql_file_path, 'r') as file:
            sql_statements = file.read()

        statements = sql_statements.split(';')

        with connection.cursor() as cursor:
            for statement in statements:
                statement = statement.strip()
                if statement:
                    if statement.lower().startswith('\\copy'):
                        self.handle_csv_import(csv_file_path)
                    else:
                        self.stdout.write(f"Executing: {statement[:50]}...")
                        cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))

    def handle_csv_import(self, csv_file_path):
        """Import the CSV file directly using Django and pandas"""
        try:
            self.stdout.write(f"Importing CSV from: {csv_file_path}")

            import csv
            from django.db import connection

            with open(csv_file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f, delimiter='|', quotechar='"')
                header = next(csv_reader)  # Skip header row

                with connection.cursor() as cursor:
                    for row in csv_reader:
                        # Properly escape values to prevent SQL injection
                        placeholders = ', '.join(['%s'] * len(row))
                        query = f"INSERT INTO b11_1_helptooltip (field_name, help_content_de, inline_help_de, help_content_fr, inline_help_fr, help_content_en, inline_help_en) VALUES ({placeholders})"
                        cursor.execute(query, row)

            self.stdout.write(self.style.SUCCESS("CSV import completed successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing CSV: {str(e)}"))

    def is_local_environment(self):
        # Use the IN_DOCKER variable from settings.py
#        return not getattr(settings, 'IN_DOCKER', False)
        return False
