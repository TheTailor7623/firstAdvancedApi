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
    # Tasks endpoints
    path("user/tasks", views.tasksApi.as_view(), name="tasks-enpoint"),
    path("user/task/new-task", views.newTaskApi.as_view(), name="new-task-endpoint"),
    path("user/task/<int:task_id>", views.taskDetailsApi.as_view(), name="task-details-endpoint"),
]
