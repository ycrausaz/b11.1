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

        file_path = os.path.join(settings.BASE_DIR, 'symm/pgsql/insert_all.txt')
        with open(file_path, 'r') as file:
            sql_statements = file.read()

        statements = sql_statements.split(';')

        with connection.cursor() as cursor:
            for statement in statements:
                statement = statement.strip()
                if statement:
                    if statement.lower().startswith('\\copy'):
                        self.handle_copy_command(statement)
                    else:
                        self.stdout.write(f"Executing: {statement[:50]}...")
                        cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))

    def handle_copy_command(self, command):
        self.stdout.write(f"Executing COPY command: {command[:50]}...")
        
        db_settings = settings.DATABASES['default']
        env = os.environ.copy()
        env['PGPASSWORD'] = db_settings['PASSWORD']
        
        psql_command = [
            'psql',
            '-h', db_settings['HOST'],
            '-p', str(db_settings['PORT']),
            '-U', db_settings['USER'],
            '-d', db_settings['NAME'],
            '-c', command
        ]
        
        try:
            result = subprocess.run(psql_command, env=env, check=True, capture_output=True, text=True)
            self.stdout.write(self.style.SUCCESS(f"COPY command executed successfully: {result.stdout}"))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Error executing COPY command: {e.stderr}"))

    def is_local_environment(self):
        # Use the IN_DOCKER variable from settings.py
#        return not getattr(settings, 'IN_DOCKER', False)
        return False
