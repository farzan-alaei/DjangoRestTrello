from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(APIView):

    def post(self, request):
        email_or_mobile = request.data.get("email_or_mobile")
        password = request.data.get("password")

        user_exists = (
            User.objects.filter(email=email_or_mobile).exists()
            or User.objects.filter(mobile=email_or_mobile).exists()
        )

        if user_exists:
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if "@" in email_or_mobile:
            user = User.objects.create_user(
                email=email_or_mobile, mobile=None, password=password
            )
            user.save()
        else:
            user = User.objects.create_user(
                mobile=email_or_mobile, email=None, password=password
            )
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
