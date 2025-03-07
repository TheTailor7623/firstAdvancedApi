"""
Database models
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class UsersModelManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, first_name, last_name, date_of_birth, city, password=None):
        """Handles creating a new user"""
        if not email:
            raise ValueError("Users must have a valid email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            city=city
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, last_name, date_of_birth, city, password):
        """Handles creating a staff user"""
        user = self.create_user(email, first_name, last_name, date_of_birth, city, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, city, password):
        """Handles creating a superuser"""
        user = self.create_user(email, first_name, last_name, date_of_birth, city, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UsersModel(AbstractBaseUser, PermissionsMixin):
    """Database user model for users in the system"""
    CITY_CHOICES = [
        # United Kingdom
        ("london", "London"),
        ("loughborough", "Loughborough"),
        ("coventry", "Coventry"),
        ("derby", "Derby"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    city = models.CharField(choices=CITY_CHOICES, max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsersModelManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "surname", "date_of_birth", "city"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_city(self):
        return self.city

    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"

class StoriesModel(models.Model):
    """Database stories model for stories in the system"""
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    story_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.created_at}"

class IncidentsModel(models.Model):
    """Database incident model for story incidents in the system"""
    story = models.OneToOneField(StoriesModel, on_delete=models.CASCADE, primary_key=True)
    incident_what = models.TextField()
    incident_where = models.CharField(max_length=255)
    incident_when = models.DateTimeField()

    def __str__(self):
        return f"Incident for {self.story.title} - {self.incident_where}"

class PeoplesModel(models.Model):
    """Database people model for people within the incidents for stories (the WHO)"""
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} - {self.type}"

class VAKSModel(models.Model):
    """Database VAKS model for VAKS within stories"""
    story = models.ForeignKey(StoriesModel, on_delete=models.CASCADE)
    vaks_id = models.AutoField(primary_key=True)
    sight = models.TextField()
    sound = models.TextField()
    smell = models.TextField()
    taste = models.TextField()
    touch = models.TextField()
    emotion = models.TextField()

class PointsModel(models.Model):
    """Database points model for different points of a story"""
    story = models.ForeignKey(StoriesModel, on_delete=models.CASCADE)
    point_id = models.AutoField(primary_key=True)
    content = models.TextField()

class ScriptsModel(models.Model):
    """Database scripts model for a story's script"""
    story = models.ForeignKey(StoriesModel, on_delete=models.CASCADE)
    script_id = models.AutoField(primary_key=True)
    content = models.TextField()

# class MediaModel(models.Model):
#     """Database media model for a story's media"""
#     story = models.ForeignKey(StoriesModel, on_delete=models.CASCADE)
#     media_id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=255)
#     media_url = models.SlugField()

class LinksModel(models.Model):
    """Database links model for a story's links"""
    link_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class CharactersModel(models.Model):
    """Database characters model for a story's links"""
    character_id = models.AutoField(primary_key=True)
    body_language = models.CharField(max_length=255)
    dialog = models.TextField()

# Junction models (they turn what would be many-to-many relationships to 2 x one-to-many relationships)
class PeopleIncidentModel(models.Model):
    """Database people and incident junction model"""
    person = models.ForeignKey(PeoplesModel, on_delete=models.CASCADE)
    incident = models.ForeignKey(IncidentsModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("person", "incident")

class StoryLinkModel(models.Model):
    """Database story and link junction model"""
    story = models.ForeignKey(StoriesModel, on_delete=models.CASCADE)
    link = models.ForeignKey(LinksModel, on_delete=models.CASCADE)

class StoryCharactersModel(models.Model):
    """Database story and characters junction model"""
    story = models.ForeignKey(StoriesModel, on_delete=models.CASCADE)
    character = models.ForeignKey(CharactersModel, on_delete=models.CASCADE)

"""
Notes for myself:
-
"""