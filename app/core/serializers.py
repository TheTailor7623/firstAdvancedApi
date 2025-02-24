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
        fields = ("email", "firstname", "surname", "date_of_birth", "city", "password", "confirm_password")
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
            firstname=validated_data["firstname"],
            surname=validated_data["surname"],
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
    firstname = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    city = serializers.ChoiceField(choices=models.UsersModel.CITY_CHOICES)
    gender = serializers.ChoiceField(choices=models.UsersModel.GENDER_CHOICES)

    # Custom update logic (crUd)
    def update(self, instance, validated_data):
        """Updates a resource and returns the updated record"""
        instance.email = validated_data.get("email", instance.email)
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.city = validated_data.get("city", instance.city)
        instance.gender = validated_data.get("gender", instance.gender)

        instance.save()

        return instance