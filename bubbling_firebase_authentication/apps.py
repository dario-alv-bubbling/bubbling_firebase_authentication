from django.apps import AppConfig
from firebase_admin import credentials, initialize_app

from bubbling_firebase_authentication.settings import firebase_auth_settings, APP_NAME


class FirebaseAuthConfig(AppConfig):
    name = APP_NAME
    verbose_name = 'Authentication with Firebase app'

    def ready(self) -> None:
        self.firebase_app = initialize_app(
            credentials.Certificate(firebase_auth_settings.SERVICE_ACCOUNT_KEY_FILE),
            name=self.name
            )
