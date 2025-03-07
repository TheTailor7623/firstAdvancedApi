from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from core import serializers, models

"""
Core application APIs
"""
# Dashboard API endpoints
class dashboardApi(APIView):
    """Api displaying all endpoints"""
    def get(self, request, format=None):
        """Handles GET requests made to the dashboard API endpoint"""
        apiEndpointList = {
            "Admin":"http://127.0.0.1:8000/admin/",
            "Dashboard":"http://127.0.0.1:8000/api/",
            "User registration":"http://127.0.0.1:8000/api/user/registration/",
            "Token/Login":"http://127.0.0.1:8000/api/user/token/",
            "Token refresh/re-login":"http://127.0.0.1:8000/api/user/token/refresh/",
            "Stories":"http://127.0.0.1:8000/api/stories/",
            "Create story":"http://127.0.0.1:8000/api/stories/create-new-story/",
            "View specific story":"http://127.0.0.1:8000/api/stories/story_id/",
            "View, create and modify a specific story incident":"http://127.0.0.1:8000/api/stories/story_id/incident/",
            "View, create a specific incident people list":"http://127.0.0.1:8000/api/stories/story_id/people/",
            "Modify a specific incident people list":"http://127.0.0.1:8000/api/stories/story_id/people/person_id/",
            "View, create or modify a specific VAKS for a story":"http://127.0.0.1:8000/api/stories/story_id/vaks/",
            "View or create a point for a story":"http://127.0.0.1:8000/api/stories/story_id/points/",
            "View update or delete a specific point for a story":"http://127.0.0.1:8000/api/stories/story_id/points/point_id/",
            "Create retrieve update or delete a script for a story":"http://127.0.0.1:8000/api/stories/story_id/script/",
            "View or create a link for a story":"http://127.0.0.1:8000/api/stories/story_id/links/",
            "View update or delete a specific link for a story":"http://127.0.0.1:8000/api/stories/story_id/links/link_id/",
            "View or create a character for a story":"http://127.0.0.1:8000/api/stories/story_id/characters/",
            "View update or delete a specific character for a story":"http://127.0.0.1:8000/api/stories/story_id/characters/character_id/",
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
    people_incident_serializer_class = serializers.PeopleIncidentSerializer
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

    def post(self, request, story_id, format=None):
        """Handles POST requests made to the people endpoint"""
        # Check user is owner of story
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors:":"Story not found or does not belong to you❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check story has an incident
        try:
            incident = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors:":"Incident not found or story does not have one❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize model to accept HTML form and raw data POST requests
        serialized_people_model = self.people_serializer_class(data=request.data)

        # Validate data
        if serialized_people_model.is_valid():
            # Create or get the person
            person, created = models.PeoplesModel.objects.get_or_create(
                **serialized_people_model.validated_data
            )

            # Create the link in the junction table (if not already linked)
            people_incident, link_created = models.PeopleIncidentModel.objects.get_or_create(
                person=person,
                incident=incident,
            )

            # Return success message
            return Response(
                {
                    "Success✅": "Person successfully added to the incident" if link_created else "Person was already linked to the incident",
                    "Person data":self.people_serializer_class(person).data
                },
                status=status.HTTP_201_CREATED,
            )

        # Return error message
        return Response(
            {"Errors❌:":serialized_people_model.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class storyPeopleApiDetails(APIView):
    """API View to manage requests made to the people endpoint for details"""
    people_serializer_class = serializers.PeopleSerializer
    people_incident_serializer_class = serializers.PeopleIncidentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id, person_id, format=None):
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

        # Check that the person exists
        try:
            person = models.PeoplesModel.objects.get(person_id=person_id)
        except models.PeoplesModel.DoesNotExist:
            return Response(
                {"Errors❌":"Person was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the person belongs to this incident (check junction table)
        try:
            people_incident = models.PeopleIncidentModel.objects.get(person=person, incident=incident)
        except models.PeopleIncidentModel.DoesNotExist:
            return Response(
                {"Errors❌": "This person is not linked to this incident"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize person
        serialized_person = self.people_serializer_class(person)

        return Response(
            {"Person": serialized_person.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, story_id, person_id, format=None):
        """Handles PUT requests made to this API endpoint"""
        # Check that story belongs to user
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors❌":"Story does not exist or you do not have access to it"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check that story has incident
        try:
            incident = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors❌":"Incident does not exist or your story does not have one"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check that the person exists
        try:
            person = models.PeoplesModel.objects.get(person_id=person_id)
        except models.PeoplesModel.DoesNotExist:
            return Response(
                {"Errors❌":"Person was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the person belongs to this incident (check junction table)
        try:
            people_incident = models.PeopleIncidentModel.objects.get(person=person, incident=incident)
        except models.PeopleIncidentModel.DoesNotExist:
            return Response(
                {"Errors❌": "This person is not linked to this incident"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize user input with person and user input
        serialized_user_input = self.people_serializer_class(person, data=request.data)
        # Validate data
        if serialized_user_input.is_valid():
            # Save data in person table
            serialized_user_input.save()

            # Return success message
            return Response(
                {
                    "Success ✅": "Person information updated",
                    "Person Data": serialized_user_input.data
                },
                status=status.HTTP_200_OK,
            )

        # Return error message
        return Response(
            {"Errors❌":serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, story_id, person_id, format=None):
        """Handles PATCH request made to this API endpoint"""
        # Check user owns story
        user = request.user

        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found or does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check story has incident
        try:
            incident = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors❌":"Incident not found or story does not have one"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check incident has person
        try:
            person = models.PeoplesModel.objects.get(person_id=person_id)
        except models.PeoplesModel.DoesNotExist:
            return Response(
                {"Errors❌":"person not found or does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the person belongs to this incident (check junction table)
        try:
            people_incident = models.PeopleIncidentModel.objects.get(person=person, incident=incident)
        except models.PeopleIncidentModel.DoesNotExist:
            return Response(
                {"Errors❌": "This person is not linked to this incident"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialise person with changes
        serialized_user_input = self.people_serializer_class(person, data=request.data, partial=True)
        # Validate data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()

            # Return success message
            return Response(
                {
                    "Success ✅": "Person information partially updated",
                    "Person Data": serialized_user_input.data
                },
                status=status.HTTP_200_OK,
            )

        # Return error message
        return Response(
            {"Errors ❌": "Information entered not valid"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, story_id, person_id, format=None):
        """Handles DELETE request made to remove a person from an incident"""
        user = request.user

        # Ensure the user owns the story
        try:
            story = models.StoriesModel.objects.get(user=user, story_id=story_id)
        except models.StoriesModel.DoesNotExist:
            return Response(
                {"Errors❌": "Story not found or does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the story has an incident
        try:
            incident = models.IncidentsModel.objects.get(story=story)
        except models.IncidentsModel.DoesNotExist:
            return Response(
                {"Errors❌": "Incident not found or the story does not have one"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the person exists
        try:
            person = models.PeoplesModel.objects.get(person_id=person_id)
        except models.PeoplesModel.DoesNotExist:
            return Response(
                {"Errors❌": "Person not found or does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the person belongs to this incident (check junction table)
        try:
            people_incident = models.PeopleIncidentModel.objects.get(person=person, incident=incident)
        except models.PeopleIncidentModel.DoesNotExist:
            return Response(
                {"Errors❌": "This person is not linked to this incident"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the link between the person and the incident
        people_incident.delete()

        return Response(
            {"Success ✅": "Person has been removed from this incident"},
            status=status.HTTP_204_NO_CONTENT,
        )

class vaksApi(APIView):
    """API endpoint to manage requests made for CRUD operations of VAKS to a story"""
    # Establish serializers
    story_serializer_class = serializers.StorySerializer
    vaks_serializer_class = serializers.VAKSSerializer

    # Establish models
    story_model_class = models.StoriesModel
    vaks_model_class = models.VAKSModel

    # Establish authentification and permission
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, format=None):
        """Handles GET methods made to this endpoint to RETRIEVE vaks of a story"""
        # Verify user owns story
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Error❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Identify VAKS of the story
        try:
            vaks = self.vaks_model_class.objects.get(story=story)
        except self.vaks_model_class.DoesNotExist:
            return Response(
                {"Error❌":"VAKS not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the data retrieved
        serialized_data = self.vaks_serializer_class(vaks)

        # Return success message with data
        return Response(
            {"VAKS retrieved✅":serialized_data.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        """Handles POST requests made to this endpoint to CREATE vaks of a story"""
        # Validate that user owns story
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Error❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialise user input entered by user
        serialized_user_input = self.vaks_serializer_class(data=request.data, context={"story":story})

        # Validate data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message
            return Response(
                {"VAKS has been saved successfully✅":serialized_user_input.data},
                status=status.HTTP_201_CREATED,
            )
        # Return error message
        return Response(
            {"VAKS failed to save❌":serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, story_id, format=None):
        """Handles PUT requests made to this endpoint to UPDATE vaks of a story"""
        # Validate user owns story
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Error❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate story has vaks
        try:
            vaks = self.vaks_model_class.objects.get(story=story)
        except self.vaks_model_class.DoesNotExist:
            return Response(
                {"Error❌":"VAKS not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize user input
        serialized_user_input = self.vaks_serializer_class(vaks, data=request.data)

        # Validate user input
        if serialized_user_input.is_valid():
            # Save user input
            serialized_user_input.save()
            # Return success message
            return Response(
                {"VAKS has been updated successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {"Error❌": "VAKS update failed", "Details": serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, story_id, format=None):
        """Handles PATCH requests made to this endpoint to UPDATE vaks of a story"""
        # Validate user owns story
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Error❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate story has vaks
        try:
            vaks = self.vaks_model_class.objects.get(story=story)
        except self.vaks_model_class.DoesNotExist:
            return Response(
                {"Error❌":"VAKS not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize user input
        serialized_user_input = self.vaks_serializer_class(vaks, data=request.data, partial=True)

        # Validate user input
        if serialized_user_input.is_valid():
            # Save user input
            serialized_user_input.save()
            # Return success message
            return Response(
                {"VAKS has been partially updated successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {"Error❌": "VAKS partial update failed", "Details": serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, story_id, format=None):
        """Handles DELETE requests to remove a story's VAKS"""
        # Ensure the user owns the story
        user = request.user

        story = self.story_model_class.objects.get(user=user, story_id=story_id)
        if not story:
            return Response(
                {"Error❌": "Story not found or does not belong to you"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the story has a VAKS
        vaks = self.vaks_model_class.objects.get(story=story)
        if not vaks:
            return Response(
                {"Error❌": "VAKS not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the VAKS entry
        vaks.delete()

        return Response(
            {"Success ✅": "VAKS has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

class pointsApi(APIView):
    """Api to handle all CRUD requests made to the points api endpoint of a story"""
    # Establish serializers
    stories_serializer_class = serializers.StorySerializer
    points_serializer_class = serializers.PointsSerializer

    # Establish models
    stories_model_class = models.StoriesModel
    points_model_class = models.PointsModel

    # Establish authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, format=None):
        # Validate that the story belongs to the user
        user = request.user

        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the points of the story
        try:
            points = self.points_model_class.objects.filter(story=story_id)
        except self.points_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Points not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the data retrieved
        serialized_data = self.points_serializer_class(points, many=True)

        # Return success message with point of the story
        return Response(
            {"Points retrieved successfully✅":serialized_data.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        # Validate that user owns the story
        user = request.user

        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize data entered by user
        serialized_user_input = self.points_serializer_class(data=request.data, context={"story":story})
        # Validate data entered
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message with data
            return Response(
                {"Points created successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return error message with errors
        return Response(
            {"Errors❌":serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class pointDetailsApi(APIView):
    """API endpoint to manage requests made for CRUD operations to a specific point of a story"""
    # Establish serializers
    stories_serializer_class = serializers.StorySerializer
    points_serializer_class = serializers.PointsSerializer

    # Establish models
    stories_model_class = models.StoriesModel
    points_model_class = models.PointsModel

    # Establish authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, point_id, format=None):
        """Handles GET requests to this API endpoint to retrieve a specific story point"""
        # Validate story belongs to user
        user = request.user

        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate point belongs to story
        try:
            point = self.points_model_class.objects.get(story=story_id, point_id=point_id)
        except self.points_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Point not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize retrieved data (point)
        serialized_retrieved_data = self.points_serializer_class(point)
        # Return success message with data (point)
        return Response(
            {"Point retrieved successfully✅:":serialized_retrieved_data.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, story_id, point_id, format=None):
        """Handles PUT requests to this API endpoint to update completely a specific story point"""
        # Validate story belongs to a user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate point belongs to a story
        try:
            point = self.points_model_class.objects.get(story=story, point_id=point_id)
        except self.points_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Point not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize the user input with the current point
        serialized_user_input = self.points_serializer_class(point, data=request.data)
        # Validate serialized data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message
            return Response(
                {"Point updated successfully✅:":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {"Errors❌":"Point update failed"},
            status=status.HTTP_404_NOT_FOUND,
        )

    def patch(self, request, story_id, point_id, format=None):
        """Handles PATCH requests to this API endpoint to partially update a specific story point"""
        # Validate story belongs to a user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate point belongs to a story
        try:
            point = self.points_model_class.objects.get(story=story, point_id=point_id)
        except self.points_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Point not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize the user input with the current point
        serialized_user_input = self.points_serializer_class(point, data=request.data, partial=True)
        # Validate serialized data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message
            return Response(
                {"Point updated successfully✅:":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {"Errors❌":"Point update failed"},
            status=status.HTTP_404_NOT_FOUND,
        )

    def delete(self, request, story_id, point_id, format=None):
        """Handles DELETE request to this API endpoint to delete a specific story point"""
        # Validate story belongs to a user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate point belongs to a story
        try:
            point = self.points_model_class.objects.get(story=story, point_id=point_id)
        except self.points_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Point not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Delete point
        point.delete()
        # Return success message
        return Response(
            {"Success ✅": "Point has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

class scriptApi(APIView):
    """API endpoint to manage requests made for CRUD operations to the script of a story"""
    # Establish serializers
    story_serializer_class = serializers.StorySerializer
    script_serializer_class = serializers.ScriptsSerializer

    # Establish models
    stories_model_class = models.StoriesModel
    scripts_model_class = models.ScriptsModel

    # Establish authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, format=None):
        # Validate story belongs to the user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate story has script
        try:
            script = self.scripts_model_class.objects.get(story=story_id)
        except self.scripts_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Script not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize retrieved script
        serialized_retrieved_data = self.script_serializer_class(script)
        # Return success message and script
        return Response(
            {"Script retrieved successfully✅":serialized_retrieved_data.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        # Validate story belongs to the user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate story does not have a script
        if self.scripts_model_class.objects.filter(story=story_id).exists():
            return Response(
                {"Errors❌":"Story already has a script"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize user input
        serialized_user_input = self.script_serializer_class(data=request.data, context={"story":story})
        # Validate serialized user input
        if serialized_user_input.is_valid():
            # Save
            serialized_user_input.save()
            # Return success message and data
            return Response(
                {"Script created successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return fail message and errors
        return Response(
            {"Script creation failed":serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, story_id, format=None):
        # Validate story belongs to the user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate story has a script
        try:
            script = self.scripts_model_class.objects.get(story=story_id)
        except self.scripts_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Script not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize user input with script
        serialized_user_input = self.script_serializer_class(script, data=request.data)
        # Validate serialized user input
        if serialized_user_input.is_valid():
            # Save
            serialized_user_input.save()
            # Return success message and data
            return Response(
                {"Script updated successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return fail message and errors
        return Response(
            {"Script update failed":serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, story_id, format=None):
        # Validate story belongs to the user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate story has a script
        try:
            script = self.scripts_model_class.objects.get(story=story_id)
        except self.scripts_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Script not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Serialize user input with script and partial set to True
        serialized_user_input = self.script_serializer_class(script, data=request.data, partial=True)
        # Validate serialized user input
        if serialized_user_input.is_valid():
            # Save
            serialized_user_input.save()
            # Return success message and data
            return Response(
                {"Script updated successfully✅":serialized_user_input.data},
                status=status.HTTP_200_OK,
            )
        # Return fail message and errors
        return Response(
            {"Script update failed":serialized_user_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, story_id, format=None):
        # Validate story belongs to the user
        user = request.user
        try:
            story = self.stories_model_class.objects.get(user=user, story_id=story_id)
        except self.stories_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate story has a script
        try:
            script = self.scripts_model_class.objects.get(story=story_id)
        except self.scripts_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Script not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Delete script
        script.delete()
        # Return success message and data
        return Response(
            {"Message":"Script has been deleted successfully✅"},
            status=status.HTTP_204_NO_CONTENT,
        )

class linksApi(APIView):
    """APIView to handles CRUD requests made to the links endpoint"""
    # Class serializers
    story_serializer_class = serializers.StorySerializer
    links_serializer_class = serializers.LinksSerializer
    story_link_serializer_class = serializers.StoryLinkSerializer

    # Class models
    story_model_class = models.StoriesModel
    links_model_class = models.LinksModel
    story_link_model_class = models.StoryLinkModel

    # Class authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, format=None):
        """Handles GET methods to the links API endpoint to RETRIEVE links"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve all link_ids belonging to the story
        try:
            links_belonging_to_story = self.story_link_model_class.objects.filter(story=story)
        except self.story_link_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Links not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Retrieve all links
        links = [story_link_record.link for story_link_record in links_belonging_to_story]

        # Retrieve data for each link_id
        serialized_retrieved_data = self.links_serializer_class(links, many=True)

        # Return success message with link data
        return Response(
            {
                "Success ✅": "Links retrieved successfully",
                "Links": serialized_retrieved_data.data
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        """Handles POST requests to CREATE a link for a story"""
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"error": "Story not found ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize input
        serialized_input = self.links_serializer_class(data=request.data)

        if serialized_input.is_valid():
            link_data = serialized_input.validated_data

            # Check if link exists, create if not
            link, _ = self.links_model_class.objects.get_or_create(**link_data)

            # Link the story and link if not already linked
            story_link, created = self.story_link_model_class.objects.get_or_create(story=story, link=link)

            return Response(
                {
                    "message": "Link successfully added to the story ✅" if created else "Link was already linked to the story",
                    "link_data": self.links_serializer_class(link).data
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": serialized_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class linkDetailsApi(APIView):
    """APIView to handle CRUD requests to the link specific endpoint"""
    # Class serializers
    story_serializer_class = serializers.StorySerializer
    links_serializer_class = serializers.LinksSerializer
    story_link_serializer_class = serializers.StoryLinkSerializer

    # Class models
    story_model_class = models.StoriesModel
    links_model_class = models.LinksModel
    story_link_model_class = models.StoryLinkModel

    # Class authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, link_id, format=None):
        """Handles GET methods to the links API endpoint to RETRIEVE links"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate link belongs to story
        try:
            link = self.story_link_model_class.objects.get(story=story, link_id=link_id)
        except self.story_link_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Link not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Retrieve all links
        link_details = self.links_model_class.objects.get(link_id=link_id)

        # Retrieve data for each link_id
        serialized_retrieved_data = self.links_serializer_class(link_details)

        # Return success message with link data
        return Response(
            {
                "Success ✅": "Link retrieved successfully",
                "Link details": serialized_retrieved_data.data
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, story_id, link_id, format=None):
        """Handles PUT requests made the the links endpoint to compeletely update a link"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate link belongs to story
        try:
            link = self.story_link_model_class.objects.get(story=story, link_id=link_id)
        except self.story_link_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Link not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the link
        link = self.links_model_class.objects.get(link_id=link_id)

        # Serialize user input with link
        serialized_user_input = self.links_serializer_class(link, data=request.data)
        # Validate serialized data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message with new link details
            return Response(
                {
                    "Success ✅": "Link updated successfully",
                    "Updated link details": serialized_user_input.data
                },
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {
                "Error ❌":"Link failed to update",
                "Error details":serialized_user_input.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, story_id, link_id, format=None):
        """Handles PUT requests made the the links endpoint to partially update a link"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate link belongs to story
        try:
            link = self.story_link_model_class.objects.get(story=story, link_id=link_id)
        except self.story_link_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Link not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the link
        link = self.links_model_class.objects.get(link_id=link_id)

        # Serialize user input with link
        serialized_user_input = self.links_serializer_class(link, data=request.data, partial=True)
        # Validate serialized data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message with new link details
            return Response(
                {
                    "Success ✅": "Link updated successfully",
                    "Updated link details": serialized_user_input.data
                },
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {
                "Error ❌":"Link failed to update",
                "Error details":serialized_user_input.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, story_id, link_id, format=None):
        """Handles DELETE request to this API endpoint to delete a specific link"""
        # Validate story belongs to a user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate link belongs to a story
        try:
            link = self.links_model_class.objects.get(story=story, link_id=link_id)
        except self.links_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Link not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Delete link
        link.delete()
        # Return success message
        return Response(
            {"Success ✅": "Link has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

class charactersApi(APIView):
    """APIView to handle CRUD requests to the characters API endpoint"""
    # Class serializers
    story_serializer_class = serializers.StorySerializer
    characters_serializer_class = serializers.CharactersSerializer
    story_character_serializer_class = serializers.StoryCharactersSerializer

    # Class models
    story_model_class = models.StoriesModel
    characters_model_class = models.CharactersModel
    story_character_model_class = models.StoryCharactersModel

    # Class authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, format=None):
        """Handles GET methods to the characters API endpoint to RETRIEVE characters"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve all character_ids belonging to the story
        try:
            characters_belonging_to_story = self.story_character_model_class.objects.filter(story=story)
        except self.story_character_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Characters not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Retrieve all characters
        characters = [story_character_record.characters for story_character_record in characters_belonging_to_story]

        # Retrieve data for each character_id
        serialized_retrieved_data = self.characters_serializer_class(characters, many=True)

        # Return success message with character data
        return Response(
            {
                "Success ✅": "Characters retrieved successfully",
                "Characters": serialized_retrieved_data.data
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, story_id, format=None):
        """Handles POST requests to CREATE a character for a story"""
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"error": "Story not found ❌"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize input
        serialized_input = self.characters_serializer_class(data=request.data)

        if serialized_input.is_valid():
            character_data = serialized_input.validated_data

            # Check if character exists, create if not
            character, _ = self.characters_model_class.objects.get_or_create(**character_data)

            # Link the story and character if not already linked
            story_character, created = self.story_character_model_class.objects.get_or_create(story=story, characters=character)

            return Response(
                {
                    "message": "Character successfully added to the story ✅" if created else "character was already linked to the story",
                    "character_data": self.characters_serializer_class(character).data
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": serialized_input.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class characterDetailsApi(APIView):
    """APIView to handle CRUD requests to the character details endpoint"""
    # Class serializers
    story_serializer_class = serializers.StorySerializer
    characters_serializer_class = serializers.CharactersSerializer
    story_character_serializer_class = serializers.StoryCharactersSerializer

    # Class models
    story_model_class = models.StoriesModel
    characters_model_class = models.CharactersModel
    story_character_model_class = models.StoryCharactersModel

    # Class authentication and permissions
    permission_classes = [IsAuthenticated,]

    def get(self, request, story_id, character_id, format=None):
        """Handles GET methods to the character details API endpoint to RETRIEVE a character"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate character belongs to story
        try:
            character = self.story_character_model_class.objects.get(story=story, character_id=character_id)
        except self.story_character_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Character not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Retrieve character details
        character_details = self.characters_model_class.objects.get(character_id=character_id)

        # Serialized retrieved data for character details
        serialized_retrieved_data = self.characters_serializer_class(character_details)

        # Return success message with character data
        return Response(
            {
                "Success ✅": "Character retrieved successfully",
                "Character details": serialized_retrieved_data.data
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, story_id, character_id, format=None):
        """Handles PUT requests made the the character details endpoint to compeletely update a character"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate character belongs to story
        try:
            link = self.story_character_model_class.objects.get(story=story, character_id=character_id)
        except self.story_character_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Character not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the character
        character = self.characters_model_class.objects.get(character_id=character_id)

        # Serialize user input with character
        serialized_user_input = self.characters_serializer_class(character, data=request.data)
        # Validate serialized data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message with new character details
            return Response(
                {
                    "Success ✅": "Character updated successfully",
                    "Updated character details": serialized_user_input.data
                },
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {
                "Error ❌":"Character failed to update",
                "Error details":serialized_user_input.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, story_id, character_id, format=None):
        """Handles PUT requests made the the character details endpoint to partially update a character"""
        # Validate story belongs to user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate character belongs to story
        try:
            character = self.story_character_model_class.objects.get(story=story, character_id=character_id)
        except self.story_character_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Character not found for this story"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the character
        character = self.characters_model_class.objects.get(character_id=character_id)

        # Serialize user input with character
        serialized_user_input = self.characters_serializer_class(character, data=request.data, partial=True)
        # Validate serialized data
        if serialized_user_input.is_valid():
            # Save data
            serialized_user_input.save()
            # Return success message with new character details
            return Response(
                {
                    "Success ✅": "Character updated successfully",
                    "Updated character details": serialized_user_input.data
                },
                status=status.HTTP_200_OK,
            )
        # Return error message
        return Response(
            {
                "Error ❌":"Character failed to update",
                "Error details":serialized_user_input.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, story_id, character_id, format=None):
        """Handles DELETE request to this API endpoint to delete a specific character"""
        # Validate story belongs to a user
        user = request.user
        try:
            story = self.story_model_class.objects.get(user=user, story_id=story_id)
        except self.story_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Story not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Validate character belongs to a story
        try:
            character = self.characters_model_class.objects.get(story=story, character_id=character_id)
        except self.characters_model_class.DoesNotExist:
            return Response(
                {"Errors❌":"Character not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Delete character
        character.delete()
        # Return success message
        return Response(
            {"Success ✅": "Character has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

"""
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTM0ODI1NiwiaWF0IjoxNzQxMjYxODU2LCJqdGkiOiIzNjQwYmI2MGVmZDI0MDZjOTIwNTY5OGY4ZTg2NjkxYyIsInVzZXJfaWQiOjJ9.Z9ilb-Zpy_rD_1aHj8ktaEf2fbblaXPoHxWtTD8_vZs",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMjczODU2LCJpYXQiOjE3NDEyNjE4NTYsImp0aSI6IjMwN2ZiOTZjMmM2ODRkNWJhOTJmM2JhZDY0Njg4NTU1IiwidXNlcl9pZCI6Mn0.CxCkOUUhSJmEsGtf2nQV7eq5qcxm5kev5Nhfpp9tLGU"
}

NOTES TO SELF:

Standard Practice:
Re-serializing the saved object is standard practice in DRF.
It ensures the response reflects the actual state of the object as stored in the database, including any modifications or auto-populated values.

# Return success message
return Response(
    {
        "Success✅": "Person successfully added to the incident" if link_created else "Person was already linked to the incident",
        "Person data":self.people_serializer_class(person).data
    },
    status=status.HTTP_201_CREATED,
)
"""