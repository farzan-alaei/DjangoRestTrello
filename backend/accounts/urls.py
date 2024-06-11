from accounts.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path("auth/api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
