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
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDEyNjk0OSwiaWF0IjoxNzQwMDQwNTQ5LCJqdGkiOiI4ZDZhNTlhODhlOGU0MTBkODE4YmYzZTRkN2Y5YWQzNyIsInVzZXJfaWQiOjJ9.UbG8z14wUy9aPkVLSHrUqOVd6sRoFn3mqYKBmARjYSA",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMDQyMzQ5LCJpYXQiOjE3NDAwNDA1NDksImp0aSI6IjQzNjAwMzZjOTE3MTQxNmFhMDFhZmFiOWZjZjI5MmEyIiwidXNlcl9pZCI6Mn0.-x20OpvzAGVRn85X4x1YC3rUi_J8qYwdYk4eX_QflKQ"
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
    """API to get a specific task"""
    serializer_class = serializers.TasksSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, task_id, format=None):
        """Handles GET requests made to the retrieve task details endpoint"""
        user = request.user
        try:
            task = models.TasksModel.objects.get(user=user, task_id=task_id)
            serialized_data = self.serializer_class(task)
            return Response({"Task details": serialized_data.data}, status=status.HTTP_200_OK)
        except models.TasksModel.DoesNotExist:
            return Response({"Task not found❌": serialized_data.errors}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, task_id, format=None):
        """Handles PUT requests made to the retrieve task details endpoint"""
        user = request.user
        task = models.TasksModel.objects.get(user=user, task_id=task_id)
        serialized_data = self.serializer_class(task, data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {
                    "Task updated successfully✅":serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "Task not updated successfully❌":serialized_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, task_id, format=None):
        """Handles PATCH requests made to the retrieve task details endpoint"""
        user = request.user
        task = models.TasksModel.objects.get(user=user, task_id=task_id)
        serialized_data = self.serializer_class(task, data=request.data, partial=True)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {
                    "Task partially updated successfully✅":serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "Task has not been partially updated sucessfully":serialized_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )