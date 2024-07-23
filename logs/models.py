# logs/models.py

from django.db import models

class LogEntry(models.Model):
    timestamp = models.DateTimeField()
    level = models.CharField(max_length=20)
    message = models.TextField()
    logger_name = models.CharField(max_length=100)
    function_name = models.CharField(max_length=100)
    line_number = models.IntegerField()

    def __str__(self):
        return f"{self.timestamp} [{self.level}] {self.message}"

    class Meta:
        app_label = 'logs'
