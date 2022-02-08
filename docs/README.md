**how to:**

1. Get your credentials
Get your admin credentials `.json` from the Firebase SDK and add them to your project in `<project_name>/settings` (or base directory) folder named as `firebase-cert.json`!

Get your web api key and add it to your local .env file.

```djangotemplate
FIREBASE_AUTH = {
    "SERVICE_ACCOUNT_KEY_FILE" = "path_to_your_credentials.json"
}

FIREBASE_API_KEY = <also retrieved from your firebase account>
```

2. Settings
The `django-rest-firebase-auth` comes with the following settings as default, which can be overridden in your project's `settings.py`.

```djangotemplate
FIREBASE_AUTH = {
    "SERVICE_ACCOUNT_KEY_FILE": "",

    # require that user has verified their email
    "EMAIL_VERIFICATION": False
}
```

3. Add `bubbling_firebase_authentication` to your INSTALLED_APPS setting like this::
```djangotemplate
    INSTALLED_APPS = [
        ...
        'bubbling_firebase_authentication',
    ]

    REST_FRAMEWORK = {
        ...
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "bubbling_firebase_authentication.authentication.FirebaseAuthentication", // when user with firebase_uuid exists 
            "bubbling_firebase_authentication.authentication.FirebaseAuthenticationAnonymous" // for anonymous authentication
        ]
        ...
    }   
```

4. Use in the app :
The user model
```djangotemplate
class User(AbstractUser, SoftDeleteModel):
    """
    The enhanced User model holding the details!
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)
    middle_name = models.CharField(max_length=50, blank=True, default='')
    ...
    firebase_uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    ...

    USERNAME_FIELD = 'email'
    FIREBASE_FIELD = 'firebase_uuid'

    ...
    def get_firebase_uid(self):
        return f'{str(self.pk)}__{str(self.firebase_uuid)}'
```

Usage in views
```djangotemplate
    from bubbling_firebase_authentication.firebase_anonymous_permissions import IsAuthenticatedAnonymous // for anonymous authentication, simply check that jwt is valid in firebase

    ...

    permission_classes = (IsAuthenticatedAnonymous,)
```

