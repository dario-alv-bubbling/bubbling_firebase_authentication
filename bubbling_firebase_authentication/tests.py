import uuid

import requests
from django.test import TestCase
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError

from firebase_auth import settings

RAW_PASSWORD = "passwd"
TEST_EMAIL = "firebasetestuser@test.com"
FIREBASE_ID = str(uuid.uuid4())


class FirebaseIntegrationTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        try:
            auth.delete_user(FIREBASE_ID)
        except UserNotFoundError as err:
            print('user has been already deleted, Err:', err)
        super().tearDownClass()

    def test_canCreateUser(self):
        data = {
            'uid': FIREBASE_ID,
            'display_name': 'Test Name',
            'email': TEST_EMAIL,
            'email_verified': RAW_PASSWORD
        }
        firebase_user = auth.create_user(**data)

        self.assertEqual(FIREBASE_ID, firebase_user.uid)
        self.assertEqual(TEST_EMAIL, firebase_user.email)

    def test_canConnect(self):
        token = auth.create_custom_token(FIREBASE_ID)
        self.assertIsNotNone(token)

    def test_canDeleteUser(self):
        self.assertIsNone(auth.delete_user(FIREBASE_ID))

    def test_canGetIdTokenUsingSignIn(self):
        id_token_request_data = {
            "email": TEST_EMAIL,
            "password": RAW_PASSWORD,
            "returnSecureToken": True
        }

        res = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_API_KEY}',
            data=id_token_request_data)

        self.assertIsNotNone(res)

    def test_canGetIdTokenUsingCustomToken(self):
        token = auth.create_custom_token(FIREBASE_ID)

        id_token_request_data = {
            "token": token,
            "returnSecureToken": True
        }
        token = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={settings.FIREBASE_API_KEY}',
            data=id_token_request_data)

        self.assertIsNotNone(token)
