from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.forms import ValidationError

User = get_user_model()


class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username:
            if "@" in username:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    raise ValidationError(
                        "Please enter a correct email address or mobile and password. "
                        "Note that both fields may be case-sensitive."
                    )
            else:
                try:
                    user = User.objects.get(mobile=username)
                except User.DoesNotExist:
                    raise ValidationError(
                        "Please enter a correct email address or mobile and password. "
                        "Note that both fields may be case-sensitive."
                    )
            if user and user.check_password(password):
                return user
            else:
                raise ValidationError(
                    "Please enter a correct email address or mobile and password. "
                    "Note that both fields may be case-sensitive."
                )

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
