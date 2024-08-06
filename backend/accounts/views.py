from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import CustomTokenObtainPairSerializer, UserSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view for obtaining access and refresh tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(APIView):
    """
    Register API view for creating new users.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Create new user.
        """
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
        elif email_or_mobile.isdigit():
            user = User.objects.create_user(
                mobile=email_or_mobile, email=None, password=password
            )
            user.save()
        else:
            return Response(
                {"error": "Email or Mobile is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    """
    Logout API view for logging out users.
    """
    def post(self, request):
        """
        Logout user.
        """
        try:
            refresh = request.data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    User detail update view for updating user details.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Get user object.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Update user details.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
