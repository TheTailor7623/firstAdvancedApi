from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from core import serializers, models

"""
Core application APIs

test2@example.com
test2
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTQ1MTQ3NSwiaWF0IjoxNzM5MzY1MDc1LCJqdGkiOiIwNmNlYjVlNjhmMDU0N2Y4ODg4YzRlZjhkYTk0ZDM4NiIsInVzZXJfaWQiOjN9.fUTsdL1Ywt20-4vNQJAE5JJMM57hgGs5TLC9hDlypss",
"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5MzY2ODc1LCJpYXQiOjE3MzkzNjUwNzUsImp0aSI6Ijk3ZmU4OGE5NDEyOTQ0MzQ5YzRhYTVmNWU4MmM3Mzk0IiwidXNlcl9pZCI6M30.ftFayfm2I9HZdd79Gst33HfgY1dJV6GpAMAoepG6bDs"
"""
# Dashboard API endpoints
class dashboardApi(APIView):
    """Api displaying all endpoints"""
    def get(self, request, format=None):
        """Handles GET requests made to the dashboard API endpoint"""
        apiEndpointList = {
            "Dashboard":"http://127.0.0.1:8000/api/dashboard",
            "User registration":"http://127.0.0.1:8000/api/users/register",
            "Token/Login":"http://127.0.0.1:8000/api/users/token",
            "Token refresh/re-login":"http://127.0.0.1:8000/api/users/token/refresh",
            "Resources":"http://127.0.0.1:8000/api/resources",
            "Create resource":"http://127.0.0.1:8000/api/resources/create-resource",
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

# Resources API endpoints
class resourcesApi(APIView):
    """Api for viewing resources from the resources mode"""
    serializer_class=serializers.ResourceSerializer
    permission_classes=[IsAuthenticated,]

    def get(self, request, format=None):
        """Handles GET requests to the resourcesCreateApi endpoint"""
        user=request.user
        # user_resources=models.ResourcesUsers.objects.filter(user=user).select_related("resource")
        user_resources=models.ResourcesUsers.objects.filter(user=user)

        # resources=[relation.resource for relation in user_resources]
        resources=[]
        for relation in user_resources:
            resources.append(relation.resource)
        serialized_data=self.serializer_class(resources, many=True)

        return Response(
            {"User resources:":serialized_data.data},
            status=status.HTTP_200_OK,
        )

class resourcesCreateApi(APIView):
    """Api for creating a resource in the resources model"""
    serializer_class=serializers.ResourceSerializer
    permission_classes=[IsAuthenticated,]

    def post(self, request, format=None):
        """Handles POST requests to the resourcesCreateApi endpoint"""
        serialized_data=self.serializer_class(data=request.data, context={"request":request})
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {"Resource creation successful✅":serialized_data.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"Resource creation unsuccessful❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )