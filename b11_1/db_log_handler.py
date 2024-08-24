import logging
from django.db import connections
from django.conf import settings

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        try:
            # Format the message
            message = self.format(record)

            # Create a database connection
            with connections['default'].cursor() as cursor:
                # Insert the log entry into the database
                cursor.execute("""
                    INSERT INTO b11_1_log_entries 
                    (timestamp, level, message) 
                    VALUES (NOW(), %s, %s)
                """, [record.levelname, message])
        except Exception:
            self.handleError(record)
