from django.apps import AppConfig
from bubbling_firebase_authentication.settings import APP_NAME


class FirebaseAuthConfig(AppConfig):
    name = APP_NAME
    verbose_name = 'Authentication with Firebase app'
