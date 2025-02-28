from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from core import serializers, models

"""
Core application APIs
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDgyNzY2MCwiaWF0IjoxNzQwNzQxMjYwLCJqdGkiOiI0N2MyNWFkMmE0Y2I0NGUxOWQ0ZGI0ZGM2OGUxNmMxOCIsInVzZXJfaWQiOjJ9.yfEpfZE1jys71Xes1jAUcfA-0X6NRHEzcX5PHG04Eug",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNzQ0ODYwLCJpYXQiOjE3NDA3NDEyNjAsImp0aSI6IjlmMDFjNDdjZGIwMjQ2MTBiOWRjYTdiYzU4YzQ1YjMwIiwidXNlcl9pZCI6Mn0.-A003fLxLfOdzwqLsq-jYaOluTVRSnsX0rOSR588ymk"
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
            "View, create and modify a specific story incident":"http://127.0.0.1:8000/api/stories/story_id/incident",
            "View, create and modify a specific incident people list":"http://127.0.0.1:8000/api/stories/story_id/people",
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

class storyIncidentApi(APIView):
    """API endpoint for incidents of a story"""
    serializer_class = serializers.IncidentsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id, format=None):
        """Method to handle GET requests to this API endpoint - retrieve a story's incident"""
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
            incident = models.IncidentsModel.objects.get(story=story)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors": "Story not found or does not belong to you❌"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors": "Incident not found or does not belong to you❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_incident = self.serializer_class(incident)
        return Response(
            {
                "Here is your incident for this story": serialized_incident.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        """Method to handle POST request to create an incident for a story"""

        user = request.user

        # Check if the story exists and belongs to the user
        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Error": "Story not found or does not belong to you ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the story already has an incident
        if models.IncidentsModel.objects.filter(story=story).exists():
            return Response(
                {"Error": "Story already has an incident ❌"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Serialize user input
        serialized_user_incident_input = self.serializer_class(data=request.data, context={"story": story})

        # Validate input
        if serialized_user_incident_input.is_valid():
            serialized_user_incident_input.save()
            return Response(
                {"Success": "Incident created successfully ✅", "Incident": serialized_user_incident_input.data},
                status=status.HTTP_201_CREATED,
            )

        # Return errors if validation fails
        return Response(
            {"Error": "Incident creation failed ❌", "Details": serialized_user_incident_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
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

    def patch(self, request, story_id, format=None):
        """Handle PATCH requests to partially update a story's incident"""
        # Check if the story belongs to the user
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {
                    "Errors":"story not found or you are not authorized to view it",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # Find corresponding incident
        incident = models.IncidentsModel.objects.get(story=story)

        # Handle PATCH
        serialized_user_input = self.serializer_class(incident, data=request.data, context={"story":story}, partial=True)

        if serialized_user_input.is_valid():
            serialized_user_input.save()
            return Response(
                {"Incident partially updated successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"Incident partial update failed❌"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, story_id, format=None):
        """Method to handle DELETE requests to delete an incident of a story"""
        user = request.user

        try:
            # Fetch the story for the logged-in user
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)

            # Try to get the incident associated with the story
            incident = models.IncidentsModel.objects.get(story=story)

        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors": "Story not found or you do not have access to it ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors": "Incident not found for this story ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # If incident is found, delete it
        incident.delete()

        return Response(
            {"Message": "Incident deleted successfully ✅"},
            status=status.HTTP_204_NO_CONTENT
        )

class storyPeopleApi(APIView):
    """API View to manage requests made to the people endpoint"""
    people_serializer_class = serializers.PeopleSerializer
    # people_incident_serializer_class = serializers.PeopleIncidentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id, format=None):
        """Handles GET requests made to the people endpoint"""
        # Ensure the user has access to the story
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors": "Story not found or you do not have access to this story ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Ensure story has an incident
        try:
            incident = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors": "Incident not found for this story ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Go through look up table and find list of people for incident
        people_incidents = models.PeopleIncidentModel.objects.filter(incident=incident)
        people = [people_incident_record.person for people_incident_record in people_incidents]  # Extract PeopleModel instances

        # Serialize list of people
        serialized_people = self.people_serializer_class(people, many=True)

        return Response(
            {"People involved in this incident (the WHO)": serialized_people.data},
            status=status.HTTP_200_OK,
        )