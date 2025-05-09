# yourapp/management/commands/fill_empty_translations.py
import os
import re
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fill empty translations with their corresponding msgid values'

    def add_arguments(self, parser):
        parser.add_argument('locale', nargs='?', default='all', help='Locale code (e.g., "de") or "all"')

    def handle(self, *args, **options):
        locale = options['locale']
        locale_dir = os.path.join('locale')
        
        if locale == 'all':
            locales = [d for d in os.listdir(locale_dir) if os.path.isdir(os.path.join(locale_dir, d))]
        else:
            locales = [locale]
        
        for loc in locales:
            po_file = os.path.join(locale_dir, loc, 'LC_MESSAGES', 'django.po')
            if os.path.exists(po_file):
                self.fill_empty_msgstr(po_file)
                self.stdout.write(self.style.SUCCESS(f'Successfully filled empty translations for {loc}'))
            else:
                self.stdout.write(self.style.WARNING(f'PO file for {loc} not found'))
    
    def fill_empty_msgstr(self, po_file_path):
        with open(po_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = r'(msgid "([^"]*)")\n(msgstr "")'
        result = re.sub(pattern, r'\1\nmsgstr "\2"', content)
        
        with open(po_file_path, 'w', encoding='utf-8') as file:
            file.write(result)
