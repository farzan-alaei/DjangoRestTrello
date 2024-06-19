from accounts.views import CustomTokenObtainPairView, RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterAPIView.as_view(), name="register"),
]
