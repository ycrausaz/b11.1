# management/commands/tm_maintenance.py
from django.core.management.base import BaseCommand
import sqlite3
import os
import datetime

# Adjust the import path based on where you place the file in your project
from your_app.path.to.translation_memory_sqlite import SQLiteTranslationMemory

class Command(BaseCommand):
    help = 'Perform maintenance on the translation memory database'

    def add_arguments(self, parser):
        parser.add_argument('--db-file', default='translation_memory.db',
                           help='Path to the translation memory SQLite database')
        parser.add_argument('--vacuum', action='store_true',
                           help='Vacuum the database to optimize storage')
        parser.add_argument('--stats', action='store_true',
                           help='Show database statistics')
        parser.add_argument('--remove-pair', nargs=2, metavar=('SOURCE_LANG', 'TARGET_LANG'),
                           help='Remove all translations for a specific language pair')
        parser.add_argument('--backup', 
                           help='Backup the database to a JSON file')
        
    def handle(self, *args, **options):
        db_file = options['db_file']
        vacuum = options['vacuum']
        stats = options['stats']
        remove_pair = options['remove_pair']
        backup = options['backup']
        
        # Check if database exists
        if not os.path.exists(db_file):
            self.stderr.write(f'Database file {db_file} does not exist')
            return
        
        tm = SQLiteTranslationMemory(db_path=db_file)
        
        if stats or not any([vacuum, remove_pair, backup]):
            # If stats is explicitly requested or no other action specified
            tm_stats = tm.get_stats()
            self.stdout.write(f'Translation Memory Stats:')
            self.stdout.write(f'Total entries: {tm_stats["total_entries"]}')
            self.stdout.write(f'Unique source strings: {tm_stats["unique_sources"]}')
            self.stdout.write(f'Database file size: {os.path.getsize(db_file) / 1024:.2f} KB')
            self.stdout.write(f'Language pairs:')
            for src_lang, tgt_lang, count in tm_stats["language_pairs"]:
                self.stdout.write(f'  {src_lang} → {tgt_lang}: {count} entries')
        
        if vacuum:
            self.stdout.write('Optimizing database...')
            conn = sqlite3.connect(db_file)
            conn.execute("VACUUM")
            conn.close()
            self.stdout.write(self.style.SUCCESS('Database vacuumed and optimized'))
            # Show the new file size
            self.stdout.write(f'New database file size: {os.path.getsize(db_file) / 1024:.2f} KB')
        
        if remove_pair:
            source_lang, target_lang = remove_pair
            self.stdout.write(f'Removing all translations for {source_lang} → {target_lang}...')
            deleted = tm.remove_language_pair(source_lang, target_lang)
            self.stdout.write(self.style.SUCCESS(f'Removed {deleted} translation entries'))
        
        if backup:
            self.stdout.write(f'Backing up database to {backup}...')
            # Create directory if it doesn't exist
            backup_dir = os.path.dirname(backup)
            if backup_dir and not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                
            count = tm.export_to_json(backup)
            self.stdout.write(self.style.SUCCESS(f'Backup completed: {count} entries saved to {backup}'))
