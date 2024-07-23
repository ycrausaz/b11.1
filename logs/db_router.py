# logs/db_router.py

class LogsDbRouter:
    """
    A router to control all database operations on models in the
    logs application.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'logs':
            return 'logs_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'logs':
            return 'logs_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'logs':
            return db == 'logs_db'
        return db == 'default'
