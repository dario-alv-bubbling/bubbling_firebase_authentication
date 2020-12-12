from django.apps import AppConfig

from firebase_admin import credentials, initialize_app
from bubbling_firebase_authentication.settings import firebase_auth_settings


class FirebaseAuthConfig(AppConfig):
    name = "bubbling_firebase_authentication"
    verbose_name = "Authentication with Firebase app"

    def ready(self) -> None:
        initialize_app(
            credentials.Certificate(firebase_auth_settings.SERVICE_ACCOUNT_KEY_FILE)
        )
