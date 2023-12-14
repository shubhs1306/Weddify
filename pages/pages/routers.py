# routers.py
class SessionRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'sessions':
            return 'accounts'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'sessions':
            return 'accounts'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'sessions':
            return db == 'accounts'

        return None
