from django.urls import path, include
from core import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Dashboard endpoints
    path("", views.dashboardApi.as_view(), name="dashboard-endpoint"),
    # User endpoints
    path("user/", views.userProfileApi.as_view(), name="user-profile-endpoint"),
    path("user/registration/", views.registerUserApi.as_view(), name="user-registration-endpoint"),
    # Authentication endpoints
    path("user/token/", TokenObtainPairView.as_view(), name="token-obtain-pair-endpoint"),
    path("user/token/refresh", TokenRefreshView.as_view(), name="token-refresh-endpoint"),
    # Story endpoints
]
