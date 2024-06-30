from accounts.views import (
    CustomTokenObtainPairView,
    RegisterAPIView,
    LogoutAPIView,
    UserDetailUpdateView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", UserDetailUpdateView.as_view(), name="profile-update"),
]
