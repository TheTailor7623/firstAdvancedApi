from django.urls import path, include
from core import views

urlpatterns = [
    path("dashboard/", views.dashboardApi.as_view(), name="dashboard-endpoint"),
    path("users/register/", views.registerUserApi.as_view(), name="user-registration-endpoint"),
    path("users/<int:user_id>", views.userProfileApi.as_view(), name="user-profile-endpoint")
]
