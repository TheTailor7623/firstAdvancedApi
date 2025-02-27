from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from core import serializers, models

"""
Core application APIs
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc0MDY1MiwiaWF0IjoxNzQwNjU0MjUyLCJqdGkiOiI0NDU1Mzk4ODE0MGI0YmQzYjk5MDljOWYxOGYxYzFjMSIsInVzZXJfaWQiOjJ9.XfRRMqgn2AFALHphptVwhUaQBGfXCYy33OTLwpIIWnM",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNjU2MDUyLCJpYXQiOjE3NDA2NTQyNTIsImp0aSI6Ijk4MDRjMjNiMzBmNTRlMGJiNGNlYWUxYzgyMWVmOTZkIiwidXNlcl9pZCI6Mn0.Z3FzeLypbCzZEE7ArEOeQXTKK_-FzSr79Ud41njjOa0"
}
"""
# Dashboard API endpoints
class dashboardApi(APIView):
    """Api displaying all endpoints"""
    def get(self, request, format=None):
        """Handles GET requests made to the dashboard API endpoint"""
        apiEndpointList = {
            "Admin":"http://127.0.0.1:8000/admin",
            "Dashboard":"http://127.0.0.1:8000/api",
            "User registration":"http://127.0.0.1:8000/api/user/registration",
            "Token/Login":"http://127.0.0.1:8000/api/user/token",
            "Token refresh/re-login":"http://127.0.0.1:8000/api/user/token/refresh",
            "Stories":"http://127.0.0.1:8000/api/stories",
            "Create story":"http://127.0.0.1:8000/api/stories/create-new-story",
            "View specific story":"http://127.0.0.1:8000/api/stories/story_id",
            "View and modify a specific story incident":"http://127.0.0.1:8000/api/stories/story_id/incident",
            "Create specific story incident":"http://127.0.0.1:8000/api/stories/story_id/incident/create-new-incident",
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
            {"User registration failed❌":serialized_data.errors},
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
            {"User profile update failed❌":serialized_data.errors},
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
            {"User profile partial update failed❌":serialized_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

# Stories API endpoints
class storiesApi(APIView):
    """Api for viewing stories"""
    serializer_class=serializers.StorySerializer
    permission_classes=[IsAuthenticated,]

    def get(self, request, format=None):
        """Method to handle GET requests to this stories api endpoint"""
        user=request.user
        queryset = models.StoriesModel.objects.filter(user=user)
        serialized_data=self.serializer_class(queryset, many=True)
        return Response(
            {
                "Here are your stories:":serialized_data.data,
            },
            status=status.HTTP_200_OK,
        )

class storyCreateApi(APIView):
    """Api for creating new stories"""
    serializer_class=serializers.StorySerializer
    permission_classes=[IsAuthenticated,]

    def post(self, request, format=None):
        """Method to handle POST requests to this stories api endpoint"""
        serialized_data = self.serializer_class(data=request.data, context={"user": request.user})
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(
                {
                    "Story created successfully✅":serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "Story creation failed❌":serialized_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class storyDetailsApi(APIView):
    """Api for viewing story details"""
    serializer_class=serializers.StorySerializer
    permission_classes=[IsAuthenticated,]

    def get(self, request, story_id, format=None):
        """Method to handle GET requests to the stories details api endpoint"""
        user=request.user

        try:
            story=models.StoriesModel.objects.get(user=user, story_id=story_id)
            serialized_data=self.serializer_class(story)
            return Response(
                {
                    "Story successfully retrieved✅":serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        except models.StoriesModel.DoesNotExist:
            return Response(
                {
                    "Error:":"Story retrieval failed❌",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, story_id, format=None):
        """Method to handle PUT requests to the stories details api endpoint (full update)"""
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Error": "Story not found ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_user_input = self.serializer_class(story, data=request.data, context={"user": user})

        if serialized_user_input.is_valid():
            serialized_user_input.save()
            return Response(
                {
                    "Story modified successfully ✅": serialized_user_input.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "Story modification failed ❌": serialized_user_input.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class storyIncidentViewAndModifyApi(APIView):
    """API endpoint for incidents of a story"""
    serializer_class = serializers.IncidentsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id, format=None):
        """Method to handle GET requests to this API endpoint - retrieve a story's incident"""
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors": "Story not found or does not belong to you ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user_incident_queryset = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors": "Incident not found❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_queryset = self.serializer_class(user_incident_queryset)

        return Response(
            {
                "Here is your incident for this story": serialized_queryset.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, story_id, format=None):
        """Handle PUT requests for completely updating a story's incident"""
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors": "We could not find this story or you do not have access to it ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            incident = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors": "Incident not found for this story ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_user_input = self.serializer_class(incident, data=request.data, context={"story": story})

        if serialized_user_input.is_valid():
            serialized_user_input.save()
            return Response(
                {"Incident saved successfully ✅": serialized_user_input.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"Incident failed to save ❌": serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class storyIncidentCreateApi(APIView):
    """API endpoint to create an incident for a story"""
    serializer_class = serializers.IncidentsSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, format=None):
        """Method to handle GET requests to this API endpoint - display story for reference to user creating the story incident"""
        user = request.user
        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {
                    "Failed to retrieve story❌":"Story does not exist or you do not have permission to view it",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serialized_story = serializers.StorySerializer(story)
        return Response(
            {
                "Story retrieved✅:":serialized_story.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        """Method to handle POST requests to this API endpoint - Create a story's incident"""
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors": "Story not found or does not belong to you ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized_user_input = self.serializer_class(data=request.data, context={"story": story})
        if serialized_user_input.is_valid():
            serialized_user_input.save()
            return Response(
                {
                    "Story incident saved successfully✅":serialized_user_input.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "Story incident creation failed❌":serialized_user_input.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )