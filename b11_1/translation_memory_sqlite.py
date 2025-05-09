# translation_memory_sqlite.py
import sqlite3
import os
from difflib import SequenceMatcher
from datetime import datetime
import json

class SQLiteTranslationMemory:
    def __init__(self, db_path='translation_memory.db'):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the SQLite database if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_text TEXT NOT NULL,
            source_language TEXT NOT NULL,
            target_language TEXT NOT NULL,
            translation TEXT NOT NULL,
            context TEXT DEFAULT '',
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create indexes for faster lookups
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_source ON translations 
        (source_language, target_language, source_text)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_translation(self, source_text, source_lang, target_lang, context=''):
        """Get an exact translation match from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT translation FROM translations 
        WHERE source_text = ? AND source_language = ? AND target_language = ? AND context = ?
        ''', (source_text, source_lang, target_lang, context))
        
        result = cursor.fetchone()
        
        if result:
            # Update last_used timestamp
            cursor.execute('''
            UPDATE translations SET last_used = CURRENT_TIMESTAMP
            WHERE source_text = ? AND source_language = ? AND target_language = ? AND context = ?
            ''', (source_text, source_lang, target_lang, context))
            conn.commit()
            
            conn.close()
            return result[0]
        
        conn.close()
        return None
    
    def find_similar_translation(self, source_text, source_lang, target_lang, threshold=0.9):
        """Find similar translations with fuzzy matching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all translations for the language pair
        cursor.execute('''
        SELECT source_text, translation, id FROM translations 
        WHERE source_language = ? AND target_language = ?
        ''', (source_lang, target_lang))
        
        results = cursor.fetchall()
        
        best_match = None
        highest_ratio = 0
        best_id = None
        
        for saved_text, translation, entry_id in results:
            ratio = SequenceMatcher(None, source_text, saved_text).ratio()
            if ratio > threshold and ratio > highest_ratio:
                highest_ratio = ratio
                best_match = translation
                best_id = entry_id
        
        if best_match and best_id:
            # Update last_used timestamp
            cursor.execute('''
            UPDATE translations SET last_used = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (best_id,))
            conn.commit()
        
        conn.close()
        return best_match, highest_ratio
    
    def store_translation(self, source_text, source_lang, target_lang, translation, context=''):
        """Store a translation in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if it already exists
        cursor.execute('''
        SELECT id FROM translations 
        WHERE source_text = ? AND source_language = ? AND target_language = ? AND context = ?
        ''', (source_text, source_lang, target_lang, context))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing translation
            cursor.execute('''
            UPDATE translations 
            SET translation = ?, last_used = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (translation, result[0]))
        else:
            # Insert new translation
            cursor.execute('''
            INSERT INTO translations
            (source_text, source_language, target_language, translation, context)
            VALUES (?, ?, ?, ?, ?)
            ''', (source_text, source_lang, target_lang, translation, context))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get statistics about the translation memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM translations')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT source_text) FROM translations')
        unique_sources = cursor.fetchone()[0]
        
        cursor.execute('SELECT source_language, target_language, COUNT(*) FROM translations GROUP BY source_language, target_language')
        language_pairs = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_entries': total,
            'unique_sources': unique_sources,
            'language_pairs': language_pairs
        }
    
    def export_to_json(self, output_file):
        """Export the database to JSON format"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT source_text, source_language, target_language, translation, context,
        created, last_used FROM translations
        ''')
        
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        conn.close()
        return len(result)
    
    def import_from_json(self, input_file):
        """Import translations from JSON format"""
        with open(input_file, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added = 0
        updated = 0
        
        for entry in entries:
            source_text = entry['source_text']
            source_lang = entry['source_language']
            target_lang = entry['target_language']
            translation = entry['translation']
            context = entry.get('context', '')
            
            # Check if it exists
            cursor.execute('''
            SELECT id FROM translations 
            WHERE source_text = ? AND source_language = ? AND target_language = ? AND context = ?
            ''', (source_text, source_lang, target_lang, context))
            
            if cursor.fetchone():
                cursor.execute('''
                UPDATE translations 
                SET translation = ?
                WHERE source_text = ? AND source_language = ? AND target_language = ? AND context = ?
                ''', (translation, source_text, source_lang, target_lang, context))
                updated += 1
            else:
                cursor.execute('''
                INSERT INTO translations
                (source_text, source_language, target_language, translation, context)
                VALUES (?, ?, ?, ?, ?)
                ''', (source_text, source_lang, target_lang, translation, context))
                added += 1
        
        conn.commit()
        conn.close()
        return added, updated
    
    def clear_database(self):
        """Clear all translations from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM translations')
        
        conn.commit()
        conn.close()
    
    def remove_language_pair(self, source_lang, target_lang):
        """Remove all translations for a specific language pair"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM translations 
        WHERE source_language = ? AND target_language = ?
        ''', (source_lang, target_lang))
        
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted
