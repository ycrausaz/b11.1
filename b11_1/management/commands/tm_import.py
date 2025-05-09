# management/commands/tm_import.py
from django.core.management.base import BaseCommand
import os

# Adjust the import path based on where you place the file in your project
from your_app.path.to.translation_memory_sqlite import SQLiteTranslationMemory

class Command(BaseCommand):
    help = 'Import translation memory from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('--db-file', default='translation_memory.db',
                           help='Path to the translation memory SQLite database')
        parser.add_argument('--input', required=True, 
                           help='Path to input JSON file')
        parser.add_argument('--clear', action='store_true',
                           help='Clear existing translation memory before import')
        
    def handle(self, *args, **options):
        db_file = options['db_file']
        input_file = options['input']
        clear = options['clear']
        
        # Check if input file exists
        if not os.path.exists(input_file):
            self.stderr.write(f'Input file {input_file} does not exist')
            return
        
        tm = SQLiteTranslationMemory(db_path=db_file)
        
        if clear:
            self.stdout.write('Clearing existing translation memory...')
            tm.clear_database()
        
        try:
            added, updated = tm.import_from_json(input_file)
            
            self.stdout.write(self.style.SUCCESS(
                f'Import completed successfully: {added} entries added, {updated} entries updated'
            ))
            
            # Show updated stats
            tm_stats = tm.get_stats()
            self.stdout.write(f'Translation Memory Stats after import:')
            self.stdout.write(f'Total entries: {tm_stats["total_entries"]}')
            self.stdout.write(f'Unique source strings: {tm_stats["unique_sources"]}')
            self.stdout.write(f'Language pairs:')
            for src_lang, tgt_lang, count in tm_stats["language_pairs"]:
                self.stdout.write(f'  {src_lang} → {tgt_lang}: {count} entries')
                
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during import: {str(e)}'))
