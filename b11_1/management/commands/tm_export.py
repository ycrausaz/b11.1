# management/commands/tm_export.py
from django.core.management.base import BaseCommand
import os

# Adjust the import path based on where you place the file in your project
from your_app.path.to.translation_memory_sqlite import SQLiteTranslationMemory

class Command(BaseCommand):
    help = 'Export translation memory to a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('--db-file', default='translation_memory.db',
                           help='Path to the translation memory SQLite database')
        parser.add_argument('--output', required=True, 
                           help='Path to output JSON file')
        parser.add_argument('--source-lang', 
                           help='Filter by source language')
        parser.add_argument('--target-lang', 
                           help='Filter by target language')
        
    def handle(self, *args, **options):
        db_file = options['db_file']
        output = options['output']
        
        # Check if database exists
        if not os.path.exists(db_file):
            self.stderr.write(f'Database file {db_file} does not exist')
            return
        
        tm = SQLiteTranslationMemory(db_path=db_file)
        count = tm.export_to_json(output)
        
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.stdout.write(self.style.SUCCESS(f'Exported {count} translation entries to {output}'))
        
        # Show stats about the export
        tm_stats = tm.get_stats()
        self.stdout.write(f'Translation Memory Stats:')
        self.stdout.write(f'Total entries: {tm_stats["total_entries"]}')
        self.stdout.write(f'Unique source strings: {tm_stats["unique_sources"]}')
        self.stdout.write(f'Language pairs:')
        for src_lang, tgt_lang, count in tm_stats["language_pairs"]:
            self.stdout.write(f'  {src_lang} → {tgt_lang}: {count} entries')
