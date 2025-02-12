from django.urls import path, include
from core import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("dashboard/", views.dashboardApi.as_view(), name="dashboard-endpoint"),
    path("users/register/", views.registerUserApi.as_view(), name="user-registration-endpoint"),
    path("users/<int:user_id>", views.userProfileApi.as_view(), name="user-profile-endpoint"),
    path("users/token/", TokenObtainPairView.as_view(), name="token-obtain-pair-endpoint"),
    path("users/token/refresh", TokenRefreshView.as_view(), name="token-refresh-endpoint")
]
