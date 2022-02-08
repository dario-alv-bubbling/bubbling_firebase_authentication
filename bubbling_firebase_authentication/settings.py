from django.conf import settings
from firebase_admin import credentials, initialize_app
from rest_framework.settings import APISettings

APP_NAME = 'bubbling_firebase_authentication'

FIREBASE_AUTH_SETTINGS = "FIREBASE_AUTH"

USER_SETTINGS = getattr(settings, FIREBASE_AUTH_SETTINGS)

DEFAULTS = {"SERVICE_ACCOUNT_KEY_FILE": "", "EMAIL_VERIFICATION": False}

IMPORT_STRINGS = ()

firebase_auth_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)

FIREBASE_API_KEY = ""

FIREBASE_AUTHENTICATION_APP = initialize_app(
                                credentials.Certificate(firebase_auth_settings.SERVICE_ACCOUNT_KEY_FILE),
                                name=APP_NAME
                                )
