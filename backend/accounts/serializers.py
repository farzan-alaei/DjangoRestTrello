from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    custom token obtain pair serializer
    """

    email_or_mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        validate custom token obtain pair serializer for authentication with email or mobile
        """
        email_or_mobile = attrs.get("email_or_mobile")
        password = attrs.get("password")

        user = None

        if "@" in email_or_mobile:
            try:
                user = User.objects.get(email=email_or_mobile)
            except User.DoesNotExist:
                raise AuthenticationFailed("Invalid email or password")
        else:
            try:
                user = User.objects.get(mobile=email_or_mobile)
            except User.DoesNotExist:
                raise AuthenticationFailed("Invalid mobile or password")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password")

        if user is None:
            raise AuthenticationFailed("Invalid mobile or email or password")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
