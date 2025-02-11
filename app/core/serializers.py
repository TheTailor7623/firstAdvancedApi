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
    password_confirmation_field = serializers.CharField(
        write_only=True,
        style={"input_type":"password"},
    )

    class Meta:
        model = models.UsersModel
        fields = ("id", "email", "firstname", "password", "password_confirmation_field")
        extra_kwargs = {
            "password":{
                "write_only":True,
                "style":{"input_type":"password"},
            }
        }

    def validate_passwords_match(self, data):
        """Ensure password entered twice for registration match"""
        if data["password"] != data["password_confirmation_field"]:
            raise serializers.ValidationError({"password":"Passwords do not match"})
        return data

    def create(self, validated_data):
        """Overrid usual create method with out custom user model manager create method to hash password"""
        validated_data.pop("password_confirmation_field")
        user = models.UsersModel.objects.create_user(
            email=validated_data["email"],
            firstname=validated_data["firstname"],
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

# Resources model serializers (GET, POST, PUT, PATCH, DELETE)
class ResourceSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the resource model"""
    resource_id = serializers.IntegerField(read_only=True)
    resource_type = serializers.ChoiceField(choices=models.ResourcesModel.resource_type_choices)
    resource_quantity = serializers.IntegerField(min_value=0, max_value=100)

    # Custom Create logic (Crud)
    def create(self, validated_data):
        """Creates a resource and returns the record"""
        return models.ResourcesModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a resource and returns the updated record"""
        instance.resource_type = validated_data.get("resource_type", instance.resource_type)
        instance.resource_quantity = validated_data.get("resource_quantity", instance.resource_quantity)

        instance.save()

        return instance

# Lifestages model serializers (GET, POST, PUT, PATCH, DELETE)
class LifestagesSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the lifestages model"""
    lifestage_id = serializers.IntegerField(read_only=True)
    lifestage_title = serializers.CharField(max_length=255)
    lifestage_description = serializers.CharField(max_length=2000, allow_blank=True)
    lifestage_start = serializers.DateField()
    lifestage_end = serializers.DateField()

    # Custom create logic (Crud)
    def create(self, validated_data):
        """Creates a lifestage and returns the record"""
        return models.LifestagesModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a lifestage and returns the updated record"""
        instance.lifestage_title = validated_data.get("lifestage_title", instance.lifestage_title)
        instance.lifestage_description = validated_data.get("lifestage_description", instance.lifestage_description)
        instance.lifestage_start = validated_data.get("lifestage_start", instance.lifestage_start)
        instance.lifestage_end = validated_data.get("lifestage_end", instance.lifestage_end)

        instance.save()

        return instance

# Areas model serializers (GET, POST, PUT, PATCH, DELETE)
class AreasSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the resource model"""
    area_id = serializers.IntegerField(read_only=True)
    area_title = serializers.CharField(max_length=255)
    area_description = serializers.CharField(allow_blank=True)
    area_importance_level = serializers.ChoiceField(choices=models.AreasModel.IMPORTANCE_LEVEL_CHOICES, max_length=15)
    area_importance_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    area_urgency_level = serializers.ChoiceField(choices=models.AreasModel.URGENCY_LEVEL_CHOICES, max_length=15)
    area_urgency_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    area_start = serializers.DateField()
    area_end = serializers.DateField()
    area_status = serializers.ChoiceField(choices=models.AreasModel.STATUS_CHOICES, max_length=10)

    # Custom create logic (Crud)
    def create(self, validated_data):
        """Creates an area and returns the record"""
        return models.AreasModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates an area and returns the updated record"""
        instance.area_title = validated_data.get("area_title", instance.area_title)
        instance.area_description = validated_data.get("area_description", instance.area_description)
        instance.area_importance_level = validated_data.get("area_importance_level", instance.area_importance_level)
        instance.area_importance_magnitude = validated_data.get("area_importance_magnitude", instance.area_importance_magnitude)
        instance.area_urgency_level = validated_data.get("area_urgency_level", instance.area_urgency_level)
        instance.area_urgency_magnitude = validated_data.get("area_urgency_magnitude", instance.area_urgency_magnitude)
        instance.area_start = validated_data.get("area_start", instance.area_start)
        instance.area_end = validated_data.get("area_end", instance.area_end)
        instance.area_status = validated_data.get("area_status", instance.area_status)

        instance.save()

        return instance

# Milestones model serializers (GET, POST, PUT, PATCH, DELETE)
class MilestonesSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the milestones model"""
    milestone_id = serializers.IntegerField(read_only=True)
    milestone_title = serializers.CharField(max_length=255)
    milestone_description = serializers.CharField(allow_blank=True)

    # Custom create logic (Crud)
    def create(self, validated_data):
        """Creates a milestone and returns the record"""
        return models.MilestonesModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a milestone and returns the updated record"""
        instance.milestone_title = validated_data.get("milestone_title", instance.milestone_title)
        instance.milestone_description = validated_data.get("milestone_description", instance.milestone_description)

        instance.save()

        return instance

# Projects model serializers (GET, POST, PUT, PATCH, DELETE)
class ProjectsSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the projects model"""
    project_id = serializers.IntegerField(read_only=True)
    project_title = serializers.CharField(max_length=255)
    project_description = serializers.CharField(allow_blank=True)
    project_importance_level = serializers.ChoiceField(choices=models.ProjectsModel.IMPORTANCE_LEVEL_CHOICES, max_length=15)
    project_importance_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    project_urgency_level = serializers.ChoiceField(choices=models.ProjectsModel.URGENCY_LEVEL_CHOICES, max_length=15)
    project_urgency_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    project_deadline = serializers.DateField()
    project_start = serializers.DateField()
    project_end = serializers.DateField()
    project_status = serializers.ChoiceField(choices=models.ProjectsModel.STATUS_CHOICES, max_length=10)

    # Custom create logic (Crud)
    def create(self, validated_data):
        """Creates a project and returns the record"""
        return models.ProjectsModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a project and returns the updated record"""
        instance.project_title = validated_data.get("project_title", instance.project_title)
        instance.project_description = validated_data.get("project_description", instance.project_description)

        instance.save()

        return instance

# Tasks model serializers (GET, POST, PUT, PATCH, DELETE)
class TasksSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the tasks model"""
    task_id = serializers.IntegerField(read_only=True)
    task_title = serializers.CharField(max_length=255)
    task_description = serializers.CharField(allow_blank=True)
    task_importance_level = serializers.ChoiceField(choices=models.TasksModel.IMPORTANCE_LEVEL_CHOICES, max_length=15)
    task_importance_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    task_urgency_level = serializers.ChoiceField(choices=models.TasksModel.URGENCY_LEVEL_CHOICES, max_length=15)
    task_urgency_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    task_deadline = serializers.DateField()
    task_start = serializers.DateField()
    task_end = serializers.DateField()
    task_status = serializers.ChoiceField(choices=models.TasksModel.STATUS_CHOICES, max_length=10)

    # Custom create logic (Crud)
    def create(self, validated_data):
        """Creates a task and returns the record"""
        return models.TasksModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a task and returns the updated record"""
        instance.task_title = validated_data.get("task_title", instance.task_title)
        instance.task_description = validated_data.get("task_description", instance.task_description)

        instance.save()

        return instance

# Subtasks model serializers (GET, POST, PUT, PATCH, DELETE)
class SubtasksSerializer(serializers.Serializer):
    """Serializer for CRUD database operations on the subtasks model"""
    subtask_id = serializers.IntegerField(read_only=True)
    subtask_title = serializers.CharField(max_length=255)
    subtask_description = serializers.CharField(allow_blank=True)
    subtask_importance_level = serializers.ChoiceField(choices=models.SubTasksModel.IMPORTANCE_LEVEL_CHOICES, max_length=15)
    subtask_importance_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    subtask_urgency_level = serializers.ChoiceField(choices=models.SubTasksModel.URGENCY_LEVEL_CHOICES, max_length=15)
    subtask_urgency_magnitude = serializers.IntegerField(min_value=0, max_value=15)
    subtask_deadline = serializers.DateField()
    subtask_start = serializers.DateField()
    subtask_end = serializers.DateField()
    subtask_status = serializers.ChoiceField(choices=models.SubTasksModel.STATUS_CHOICES, max_length=10)

    # Custom create logic (Crud)
    def create(self, validated_data):
        """Creates a subtask and returns the record"""
        return models.SubTasksModel.objects.create(**validated_data)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a subtask and returns the updated record"""
        instance.subtask_title = validated_data.get("subtask_title", instance.subtask_title)
        instance.subtask_description = validated_data.get("subtask_description", instance.subtask_description)

        instance.save()

        return instance