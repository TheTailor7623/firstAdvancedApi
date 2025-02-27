"""
Contains all serializers for the core application
"""
from rest_framework import serializers
from core import models
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

# User model serializers
class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for registration of a new user in our user model"""
    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type":"password"},
    )

    class Meta:
        model = models.UsersModel
        fields = ("email", "first_name", "last_name", "date_of_birth", "city", "password", "confirm_password")
        extra_kwargs = {
            "password":{
                "write_only":True,
                "style":{"input_type":"password"},
            }
        }

    def validate(self, data):
        """Ensure password entered twice for registration match"""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password":"Passwords do not match"})
        return data

    def create(self, validated_data):
        """Overrid usual create method with out custom user model manager create method to hash password"""
        validated_data.pop("confirm_password")
        user = models.UsersModel.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            date_of_birth=validated_data["date_of_birth"],
            city=validated_data["city"],
            password=validated_data["password"]
        )
        return user

class LoginUserSerializer(serializers.Serializer):
    """Serializer for login of a user in our user model"""
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        """Validates user credentials"""
        email = data["email"]
        password = data["password"]

        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid credentials")
        return {
            "user": user,
            "token": Token.objects.get(user=user).key,
        }

class UserProfileSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the user model"""
    user_id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    city = serializers.ChoiceField(choices=models.UsersModel.CITY_CHOICES)
    gender = serializers.ChoiceField(choices=models.UsersModel.GENDER_CHOICES)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a resource and returns the updated record"""
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.city = validated_data.get("city", instance.city)
        instance.gender = validated_data.get("gender", instance.gender)

        instance.save()

        return instance

# Stories serializers
class StorySerializer(serializers.Serializer):
    """Serializer for stories model"""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    story_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """Function to create an object within the model"""
        user=self.context["user"]
        return models.StoriesModel.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        #validated_data is a dictionary
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        return instance

class IncidentsSerializer(serializers.Serializer):
    """Serializer for incidents model"""
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    incident_id = serializers.IntegerField(read_only=True)
    incident_what = serializers.CharField()
    incident_where = serializers.CharField(max_length=255)
    incident_when = serializers.DateTimeField()

    def create(self, validated_data):
        """Create an incident and assign it to the correct story"""
        story = self.context.get("story")

        if not story:
            raise serializers.ValidationError({"story": "Story must be provided ❌"})

        return models.IncidentsModel.objects.create(story=story, **validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.incident_what = validated_data.get("incident_what", instance.incident_what)
        instance.incident_where = validated_data.get("incident_where", instance.incident_where)
        instance.incident_when = validated_data.get("incident_when", instance.incident_when)
        instance.save()
        return instance

class PeopleSerializer(serializers.Serializer):
    """Serializer for peoples model"""
    person_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """Function to create an object within the model"""
        return models.PeoplesModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.type = validated_data.get("type", instance.type)

        instance.save()
        return instance

class VAKSSerializer(serializers.Serializer):
    """Serializer for VAKS model"""
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    vaks_id = serializers.IntegerField(read_only=True)
    sight = serializers.CharField()
    height = serializers.CharField()
    smell = serializers.CharField()
    taste = serializers.CharField()
    touch = serializers.CharField()
    emotion = serializers.CharField()

    def create(self, validated_data):
        """Function to create an object within the model"""
        return models.VAKSModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.sight = validated_data.get("sight", instance.sight)
        instance.height = validated_data.get("height", instance.height)
        instance.smell = validated_data.get("smell", instance.smell)
        instance.taste = validated_data.get("taste", instance.taste)
        instance.touch = validated_data.get("touch", instance.touch)
        instance.emotion = validated_data.get("emotion", instance.emotion)

        instance.save()
        return instance

class PointsSerializer(serializers.Serializer):
    """Serializer for Points model"""
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    point_id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()

    def create(self, validated_data):
        """Function to create an object within the model"""
        return models.PointsModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.content = validated_data.get("content", instance.content)

        instance.save()
        return instance

class ScriptsSerializer(serializers.Serializer):
    """Serializer for script model"""
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    script_id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()

    def create(self, validated_data):
        """Function to create an object within the model"""
        return models.ScriptsModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.content = validated_data.get("content", instance.content)

        instance.save()
        return instance

class MediaSerializer(serializers.Serializer):
    """Serializer for media model"""
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    media_id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(max_length=255)
    media_url = serializers.SlugField()

    def create(self, validated_data):
        """Function to create an object within the model"""
        return models.MediaModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.type = validated_data.get("type", instance.type)
        instance.media_url = validated_data.get("media_url", instance.media_url)

        instance.save()
        return instance

class LinksSerializer(serializers.Serializer):
    """Serializer for link model"""
    link_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    colour = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """Function to create an object within the model"""
        return models.LinksModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update an object within the model"""
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.colour = validated_data.get("colour", instance.colour)

        instance.save()
        return instance

class CharactersSerializer(serializers.Serializer):
    """Serializer for character model"""
    character_id = serializers.IntegerField(read_only=True)
    body_language = serializers.CharField(max_length=255)
    dialog = serializers.CharField()

    def create(self, validated_data):
        """Function to create object within the model"""
        return models.CharactersModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Function to update object within the model"""
        instance.body_language = validated_data.get("body_language", instance.body_language)
        instance.dialog = validated_data.get("dialog", instance.dialog)

        instance.save()
        return instance

# Junction models serializers
class PeopleIncidentSerializer(serializers.Serializer):
    """Serializer for the people and incident junction model"""
    person = serializers.PrimaryKeyRelatedField(queryset=models.PeoplesModel.objects.all())
    incident = serializers.PrimaryKeyRelatedField(queryset=models.IncidentsModel.objects.all())

    def create(self, validated_data):
        return models.PeopleIncidentModel.objects.create(**validated_data)

class StoryLinkSerializer(serializers.Serializer):
    """Serializer for the story and link junction model"""
    story = serializers.PrimaryKeyRelatedField(queryset=models.StoriesModel.objects.all())
    link = serializers.PrimaryKeyRelatedField(queryset=models.LinksModel.objects.all())

    def create(self, validated_data):
        return models.StoryLinkModel.objects.create(**validated_data)

class StoryCharactersSerializer(serializers.Serializer):
    """Serializer for the story and characters junction model"""
    story = serializers.PrimaryKeyRelatedField(queryset=models.StoriesModel.objects.all())
    characters = serializers.PrimaryKeyRelatedField(queryset=models.CharactersModel.objects.all())

    def create(self, validated_data):
        return models.StoryCharactersModel.objects.create(**validated_data)