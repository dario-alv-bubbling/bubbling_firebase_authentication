from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from firebase_admin import auth, credentials

from bubbling_firebase_authentication.settings import firebase_auth_settings, APP_NAME

User = get_user_model()


class BaseFirebaseAuthentication(BaseAuthentication):
    """
    Base implementation of token based authentication using firebase.
    """

    www_authenticate_realm = "api"
    auth_header_prefix = "Bearer"
    uid_field = getattr(User, 'FIREBASE_FIELD', None)
    uid_separator = '__'

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and decoded firebase payload if a valid signature
        has been supplied. Otherwise returns `None`.
        """
        firebase_token = self.get_token(request)

        if not firebase_token:
            return None

        try:
            payload = auth.verify_id_token(firebase_token,
                                           app=apps.get_app_config(APP_NAME).firebase_app,
                                           check_revoked=True)
        except ValueError:
            msg = _("Invalid firebase ID token.")
            raise exceptions.AuthenticationFailed(msg)
        except (
            auth.ExpiredIdTokenError,
            auth.InvalidIdTokenError,
            auth.RevokedIdTokenError,
        ):
            msg = _("Could not authenticate")
            raise exceptions.AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload)

        return user, payload

    def get_token(self, request):
        """
        Returns the firebase ID token from request.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.auth_header_prefix.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid Authorization header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_credentials(self, payload):
        """
        Returns an user that matches the payload's user uid and email.
        """
        if payload["firebase"]["sign_in_provider"] == "anonymous":
            msg = _("Firebase anonymous sign-in is not supported.")
            raise exceptions.AuthenticationFailed(msg)

        if firebase_auth_settings.EMAIL_VERIFICATION:
            if not payload["email_verified"]:
                msg = _("User email not yet confirmed.")
                raise exceptions.AuthenticationFailed(msg)

        try:
            user = self.get_user(payload["uid"])
        except User.DoesNotExist:
            msg = _("User does not exist.")
            raise exceptions.AuthenticationFailed(msg)

        return user

    def get_user(self, uid: str) -> User:
        """Returns the user with given uid"""
        raise NotImplementedError(".get_user() must be overriden.")

    def create_user_from_firebase(
        self, uid: str, firebase_user: auth.UserRecord
    ) -> User:
        """Creates a new user with firebase info"""
        raise NotImplementedError(".create_user_from_firebase() must be overriden.")

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(self.auth_header_prefix, self.www_authenticate_realm)


class FirebaseAuthentication(BaseFirebaseAuthentication):
    """
    Token based authentication using firebase.

    Clients should authenticate by passing a Firebase ID token in the
    Authorization header using Bearer scheme.
    """

    def get_user(self, uid: str) -> User:
        uid_strings = uid.split(self.uid_separator)  # [user id , firebase uuid]
        return User.objects.get(**{self.uid_field: uid_strings[1]})

    def create_user_from_firebase(
        self, uid: str, firebase_user: auth.UserRecord
    ) -> User:
        fields = {self.uid_field: uid, "email": firebase_user.email}

        return User.objects.create(**fields)


class FirebaseAuthenticationAnonymous(BaseFirebaseAuthentication):
    """
    Token based authentication using firebase.

    Clients should authenticate by passing a Firebase ID token in the
    Authorization header using Bearer scheme.
    """

    def get_user(self, uid: str) -> AnonymousUser:
        uid_strings = uid.split(self.uid_separator)  # [user id , firebase uuid]
        user = AnonymousUser()
        user.id = uid_strings[0]
        setattr(user, 'uuid', uid_strings[1])
        return user

    def create_user_from_firebase(
        self, uid: str, firebase_user: auth.UserRecord
    ):
        pass
