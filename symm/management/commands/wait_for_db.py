import time
import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                # Try to connect to both databases
                for db_name, db_config in settings.DATABASES.items():
                    self.stdout.write(f"Attempting to connect to {db_name} database at {db_config['HOST']}:{db_config['PORT']}")
                    conn = psycopg2.connect(
                        dbname=db_config['NAME'],
                        user=db_config['USER'],
                        password=db_config['PASSWORD'],
                        host=db_config['HOST'],
                        port=db_config['PORT'],
                        connect_timeout=1,
                        sslmode='disable'
                    )
                    conn.close()
                    self.stdout.write(self.style.SUCCESS(f'Successfully connected to {db_name} database'))
                db_up = True
            except psycopg2.OperationalError as e:
                self.stdout.write(f'Database unavailable: {str(e)}')
                self.stdout.write('Waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Databases available!'))
