from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from core import serializers, models

"""
Core application APIs
test@example.com
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1NzI0OCwiaWF0IjoxNzM5OTcwODQ4LCJqdGkiOiI3MzQ5YzMzODE3Njc0YzcyYTRlMTY3YjExNGNkZTBmMCIsInVzZXJfaWQiOjJ9.Q-yPFANXaiLQOR-IBTbeZ9xZqVQa5dgO4hA_X-SvByY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5OTcyNjQ4LCJpYXQiOjE3Mzk5NzA4NDgsImp0aSI6IjU5Mzk3MmQ3YjAxMjQ4YjNiODBmYzgzNWQ4ZDBlZmUzIiwidXNlcl9pZCI6Mn0.QEal0-mFEAP-4XXJJtzP9EU-3PkBeIuQhO4WMWe9oss"
}
"""
# Dashboard API endpoints
class dashboardApi(APIView):
    """Api displaying all endpoints"""
    def get(self, request, format=None):
        """Handles GET requests made to the dashboard API endpoint"""
        apiEndpointList = {
            "Dashboard":"http://127.0.0.1:8000/api/dashboard",
            "User registration":"http://127.0.0.1:8000/api/user/registration",
            "Token/Login":"http://127.0.0.1:8000/api/user/token",
            "Token refresh/re-login":"http://127.0.0.1:8000/api/user/token/refresh",
            "Tasks":"http://127.0.0.1:8000/api/user/tasks",
            "Create task":"http://127.0.0.1:8000/api/user/task/new-task",
            "Specific task":"http://127.0.0.1:8000/api/user/task/task_id",
        }

        return Response(
            {
                "List of API endpoints:":apiEndpointList,
            },
            status=status.HTTP_200_OK
        )

# User API endpoints
class registerUserApi(APIView):
    """Api for user registration"""
    serializer_class=serializers.RegisterUserSerializer

    def post(self, request, format=None):
        """Handles POST requests made to the user registration API endpoint"""
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {"User registration successful✅":serialized_data.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"User registration unsuccessful❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class userProfileApi(APIView):
    """Api for viewing user profile"""
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        """Handles GET requests to the user profile API endpoint"""
        user = request.user
        serialized_data = self.serializer_class(user)
        return Response({"User information": serialized_data.data}, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        """Handles PUT requests to the user profile API endpoint"""
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {"User profile update successful✅":serialized_data.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"User profile update unsuccessful❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, format=None):
        """Handles PATCH requests to the user profile endpoint"""

        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {"User profile partially update successful✅":serialized_data.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"User profile partial update unsuccessful❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class tasksApi(APIView):
    """Api for viewing user tasks"""
    serializer_class = serializers.TasksSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        """Handles GET requests to the tasks api endpoint"""
        user = request.user
        tasks = models.TasksModel.objects.filter(user=user)
        serialized_data = self.serializer_class(tasks, many=True)
        if serialized_data.is_valid:
            return Response(
                {"Tasks:":serialized_data.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"Retrieval of user tasks unsuccessful❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class newTaskApi(APIView):
    """Api for creating new tasks"""
    serializer_class = serializers.TasksSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        serialized_data = self.serializer_class(data=request.data, context={"user":request.user})
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {
                    "Task saved successfully✅":serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "Task information invalid❌":serialized_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class taskDetailsApi(APIView):
    """Api to update a task for a specific user"""
    serializer_class = serializers.TasksSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, task_id, format=None):
        """Handles GET request to the task details api endpoint"""
        user = request.user
        task = models.TasksModel.objects.filter(user=user, task_id=task_id)
        serialized_data = self.serializer_class(data=task)

        if serialized_data.is_valid():
            return Response(
                {"Task details:":serialized_data.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"Task not retrieved successfully❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )