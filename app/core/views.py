from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from core import serializers, models

"""
Core application APIs

12/02/2025
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTQ0NDA5MywiaWF0IjoxNzM5MzU3NjkzLCJqdGkiOiJhMTczMzFjZWYzZjk0ZjZlYjk0ZGRiMWQ1NjhmZTVkOSIsInVzZXJfaWQiOjF9.itbhF4ncWP_trTvBTDSziy8hpeyC0cGuwb9BUb_Pygw",
"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5MzU5NDkzLCJpYXQiOjE3MzkzNTc2OTMsImp0aSI6IjhlNWQxZDVkNTcxMDRmZDA4OTVhNTMxNWViOTk1OGQ3IiwidXNlcl9pZCI6MX0.ymL4hzPwbbzaWzOMDYqjkBfnnNRywpH8iyAdZo87aDo"
"""
# Dashboard API
class dashboardApi(APIView):
    """Api displaying all endpoints"""
    def get(self, request, format=None):
        """Handles GET requests made to the dashboard API endpoint"""
        apiEndpointList = {
            "Dashboard":"http://127.0.0.1:8000/api/dashboard",
            "User registration":"http://127.0.0.1:8000/api/users/register",
            "Token/Login":"http://127.0.0.1:8000/api/users/token",
            "Token refres/re-login":"http://127.0.0.1:8000/api/users/token/refresh",
        }

        return Response(
            {
                "List of API endpoints:":apiEndpointList,
            },
            status=status.HTTP_200_OK
        )

# User APIs
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
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        """Handles GET requests to the user profile API endpoint"""
        try:
            user = models.UsersModel.objects.get(user_id=user_id)
        except models.UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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