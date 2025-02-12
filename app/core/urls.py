from django.urls import path, include
from core import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Dashboard endpoints
    path("dashboard/", views.dashboardApi.as_view(), name="dashboard-endpoint"),
    # User endpoints
    path("users/register/", views.registerUserApi.as_view(), name="user-registration-endpoint"),
    path("users/", views.userProfileApi.as_view(), name="user-profile-endpoint"),
    # Authentication endpoints
    path("users/token/", TokenObtainPairView.as_view(), name="token-obtain-pair-endpoint"),
    path("users/token/refresh", TokenRefreshView.as_view(), name="token-refresh-endpoint"),
    # Resources endpoints
    path("resources/", views.resourcesApi.as_view(), name="resources-endpoint"),
    path("resources/create-resource", views.resourcesCreateApi.as_view(), name="resources-create-endpoint"),
]
