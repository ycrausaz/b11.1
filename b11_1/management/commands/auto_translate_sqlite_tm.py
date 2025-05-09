# management/commands/auto_translate_sqlite_tm.py
from django.core.management.base import BaseCommand
import polib
import os
import time
from django.conf import settings
import deepl

# Adjust the import path based on where you place the file in your project
from b11_1.translation_memory_sqlite import SQLiteTranslationMemory

class Command(BaseCommand):
    help = 'Automatically translate .po files using SQLite-based Translation Memory with DeepL'

    def add_arguments(self, parser):
        parser.add_argument('--languages', nargs='+', default=['en', 'fr'],
                           help='Languages to translate to')
        parser.add_argument('--db-file', default='translation_memory.db',
                           help='Path to the translation memory SQLite database')
        parser.add_argument('--fuzzy-threshold', type=float, default=0.9,
                           help='Threshold for fuzzy matching (0.0-1.0)')
        parser.add_argument('--api-key', required=True,
                           help='DeepL API key')
        parser.add_argument('--batch-size', type=int, default=50,
                           help='Number of strings to translate in one batch')
        parser.add_argument('--no-api', action='store_true',
                           help='Do not use API, only translation memory')
        parser.add_argument('--source-lang', default='de',
                           help='Source language code (default: de for German)')

    def handle(self, *args, **options):
        languages = options['languages']
        db_file = options['db_file']
        threshold = options['fuzzy_threshold']
        api_key = options['api_key']
        batch_size = options['batch_size']
        no_api = options['no_api']
        source_lang = options['source_lang']
        
        # Initialize DeepL translator if using API
        translator = None
        if not no_api:
            try:
                translator = deepl.Translator(api_key)
                usage = translator.get_usage()
                if usage.character.limit:
                    self.stdout.write(f'DeepL API usage: {usage.character.count}/{usage.character.limit} characters')
                else:
                    self.stdout.write(f'DeepL API usage: {usage.character.count} characters')
            except Exception as e:
                self.stderr.write(f'Error initializing DeepL API: {str(e)}')
                self.stderr.write('Continuing with translation memory only')
                no_api = True
        
        # Initialize translation memory
        tm = SQLiteTranslationMemory(db_path=db_file)
        
        # Statistics
        stats = {
            'total': 0,
            'tm_exact': 0,
            'tm_fuzzy': 0,
            'api': 0,
            'skipped': 0,
        }
        
        for lang in languages:
            self.stdout.write(f'Translating to {lang}...')
            po_file = os.path.join(settings.BASE_DIR, f'locale/{lang}/LC_MESSAGES/django.po')
            
            if not os.path.exists(po_file):
                self.stderr.write(f'File {po_file} does not exist')
                continue
                
            po = polib.pofile(po_file)
            
            # Collect untranslated entries for batch processing
            batch_entries = []
            batch_texts = []
            
            for entry in po:
                if not entry.translated() and entry.msgid:
                    stats['total'] += 1
                    german_text = entry.msgid
                    context = entry.msgctxt or ''
                    
                    # Try exact match in translation memory
                    translation = tm.get_translation(german_text, source_lang, lang, context)
                    
                    if translation:
                        entry.msgstr = translation
                        self.stdout.write(f'[TM EXACT] {german_text[:40]}{"..." if len(german_text) > 40 else ""} → {translation[:40]}{"..." if len(translation) > 40 else ""}')
                        stats['tm_exact'] += 1
                    else:
                        # Try fuzzy match
                        similar, ratio = tm.find_similar_translation(german_text, source_lang, lang, threshold)
                        
                        if similar:
                            entry.msgstr = similar
                            # Mark as fuzzy in PO file
                            if 'fuzzy' not in entry.flags:
                                entry.flags.append('fuzzy')
                            self.stdout.write(f'[TM FUZZY {ratio:.2f}] {german_text[:40]}{"..." if len(german_text) > 40 else ""} → {similar[:40]}{"..." if len(similar) > 40 else ""}')
                            stats['tm_fuzzy'] += 1
                        elif not no_api:
                            # Add to batch for API translation
                            batch_entries.append(entry)
                            batch_texts.append(german_text)
                            
                            # Process batch when it reaches the batch size
                            if len(batch_texts) >= batch_size:
                                self._process_batch(translator, batch_texts, batch_entries, source_lang, lang, tm, stats)
                                batch_entries = []
                                batch_texts = []
                        else:
                            stats['skipped'] += 1
            
            # Process any remaining batch items
            if batch_texts and not no_api:
                self._process_batch(translator, batch_texts, batch_entries, source_lang, lang, tm, stats)
            
            po.save()
            self.stdout.write(f'Translations for {lang} completed')
        
        # Print statistics
        self.stdout.write(f'\nTranslation Statistics:')
        self.stdout.write(f'Total strings processed: {stats["total"]}')
        if stats["total"] > 0:  # Avoid division by zero
            self.stdout.write(f'Exact TM matches: {stats["tm_exact"]} ({stats["tm_exact"]/stats["total"]*100:.1f}%)')
            self.stdout.write(f'Fuzzy TM matches: {stats["tm_fuzzy"]} ({stats["tm_fuzzy"]/stats["total"]*100:.1f}%)')
            self.stdout.write(f'API translations: {stats["api"]} ({stats["api"]/stats["total"]*100:.1f}%)')
            self.stdout.write(f'Skipped: {stats["skipped"]} ({stats["skipped"]/stats["total"]*100:.1f}%)')
        
        # Show TM database stats
        tm_stats = tm.get_stats()
        self.stdout.write(f'\nTranslation Memory Stats:')
        self.stdout.write(f'Total entries: {tm_stats["total_entries"]}')
        self.stdout.write(f'Unique source strings: {tm_stats["unique_sources"]}')
        self.stdout.write(f'Language pairs:')
        for src_lang, tgt_lang, count in tm_stats["language_pairs"]:
            self.stdout.write(f'  {src_lang} → {tgt_lang}: {count} entries')
    
    def _process_batch(self, translator, texts, entries, source_lang, target_lang, tm, stats):
        """Process a batch of texts with DeepL API"""
        try:
            # Convert language codes for DeepL
            deepl_source = self._convert_to_deepl_lang(source_lang)
            deepl_target = self._convert_to_deepl_lang(target_lang)
            
            self.stdout.write(f'Translating batch of {len(texts)} texts with DeepL...')
            
            results = translator.translate_text(
                texts,
                source_lang=deepl_source,
                target_lang=deepl_target,
                preserve_formatting=True
            )
            
            for i, result in enumerate(results):
                entries[i].msgstr = result.text
                
                # Store in translation memory
                tm.store_translation(
                    texts[i],
                    source_lang,
                    target_lang,
                    result.text,
                    entries[i].msgctxt or ''
                )
                
                self.stdout.write(f'[API] {texts[i][:40]}{"..." if len(texts[i]) > 40 else ""} → {result.text[:40]}{"..." if len(result.text) > 40 else ""}')
                stats['api'] += 1
            
            # Slight delay to avoid hitting API limits
            time.sleep(0.1)
            
        except Exception as e:
            self.stderr.write(f'DeepL API Error: {str(e)}')
            for entry in entries:
                stats['skipped'] += 1
    
    def _convert_to_deepl_lang(self, lang_code):
        """Convert Django language code to DeepL format"""
        # Language code mapping
        mapping = {
            'en': 'EN-US',  # Or EN-GB based on preference
            'fr': 'FR',
            'de': 'DE',
        }
        
        # Handle language variants (e.g., en-us -> EN-US)
        if '-' in lang_code:
            base, variant = lang_code.split('-', 1)
            return f"{base.upper()}-{variant.upper()}"
        
        # Return mapped code or uppercase if not in mapping
        return mapping.get(lang_code.lower(), lang_code.upper())
