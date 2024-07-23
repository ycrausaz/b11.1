from logging import Handler
from django.utils import timezone
#from logs.models import LogEntry

class DatabaseLogHandler(Handler):
    def emit(self, record):
        from logs.models import LogEntry
        LogEntry.objects.create(
            timestamp=timezone.now(),
            level=record.levelname,
            message=self.format(record),
            logger_name=record.name,
            function_name=record.funcName,
            line_number=record.lineno,
        )
