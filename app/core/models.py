"""
Database models
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator

class UsersModelManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, firstname, surname, date_of_birth, city, password=None):
        """Handles creating a new user"""
        if not email:
            raise ValueError("Users must have a valid email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            firstname=firstname,
            surname=surname,
            date_of_birth=date_of_birth,
            city=city
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, firstname, surname, date_of_birth, city, password):
        """Handles creating a staff user"""
        user = self.create_user(email, firstname, surname, date_of_birth, city, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, surname, date_of_birth, city, password):
        """Handles creating a superuser"""
        user = self.create_user(email, firstname, surname, date_of_birth, city, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UsersModel(AbstractBaseUser, PermissionsMixin):
    """Database user model for users in the system"""
    CITY_CHOICES = [
        # United Kingdom
        ("london", "London"),
        ("manchester", "Manchester"),
        ("birmingham", "Birmingham"),
        ("glasgow", "Glasgow"),
        ("edinburgh", "Edinburgh"),

        # United States
        ("new_york", "New York"),
        ("los_angeles", "Los Angeles"),
        ("chicago", "Chicago"),
        ("houston", "Houston"),
        ("miami", "Miami"),

        # Europe
        ("paris", "Paris"),
        ("berlin", "Berlin"),
        ("madrid", "Madrid"),
        ("rome", "Rome"),
        ("amsterdam", "Amsterdam"),
        ("vienna", "Vienna"),
        ("copenhagen", "Copenhagen"),
        ("stockholm", "Stockholm"),

        # Asia
        ("tokyo", "Tokyo"),
        ("seoul", "Seoul"),
        ("beijing", "Beijing"),
        ("shanghai", "Shanghai"),
        ("hong_kong", "Hong Kong"),
        ("singapore", "Singapore"),
        ("bangkok", "Bangkok"),
        ("mumbai", "Mumbai"),
        ("delhi", "Delhi"),
        ("jakarta", "Jakarta"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
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
        return f"{self.firstname} {self.surname}"

    def get_city(self):
        return self.city

    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"

class TasksModel(models.Model):
    """Database model for tasks"""
    IMPORTANCE_LEVEL_CHOICES = [
        ("high", "High"),
        ("intermediate", "Intermediate"),
        ("low", "Low"),
    ]

    URGENCY_LEVEL_CHOICES = [
        ("high", "High"),
        ("intermediate", "Intermediate"),
        ("low", "Low"),
    ]

    STATUS_CHOICES = [
        ("to-do", "To-do"),
        ("doing", "Doing"),
        ("done", "Done"),
    ]

    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE, related_name="tasks")
    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=255)
    task_description = models.TextField()
    task_importance_level = models.CharField(choices=IMPORTANCE_LEVEL_CHOICES, max_length=15)
    task_importance_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
    task_urgency_level = models.CharField(choices=URGENCY_LEVEL_CHOICES, max_length=15)
    task_urgency_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
    task_deadline = models.DateTimeField()
    task_start = models.DateTimeField()
    task_end = models.DateTimeField()
    task_status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    # Missing task_tags (under review for normalisation of DB)

"""
Notes for myself:
- Review task_tags they might need to become a model since they are not atomic the user is entering multiple values
- Review resource_allocation it might need to become a model since they are not atomic the user is entering multiple values
"""

# class LifestagesModel(models.Model):
#     """Database model for life stages"""
#     lifestage_id = models.AutoField(primary_key=True)
#     lifestage_title = models.CharField(max_length=255)
#     lifestage_description = models.TextField()
#     lifestage_start = models.DateField()
#     lifestage_end = models.DateField()

#     def lifestage_duration(self):
#         return (self.lifestage_end - self.lifestage_start).days

#     def __str__(self):
#         return self.lifestage_title

# class ResourcesModel(models.Model):
#     """Database model for resources"""
#     resource_type_choices = [
#         ("time", "Time"),
#         ("physical ability", "Physical ability"),
#         ("mental ability", "Mental ability"),
#         ("technology", "Technology"),
#         ("human resources", "Human resources"),
#         ("financial resources", "Financial resources"),
#     ]

#     resource_id = models.AutoField(primary_key=True)
#     resource_type = models.CharField(choices=resource_type_choices, max_length=30)
#     resource_quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
#     # Missing resource_allocation (under review for normalisation of DB)

#     def __str__(self):
#         return f"{self.resource_id} - {self.resource_type}"

# class MilestonesModel(models.Model):
#     """Database model for milestones"""
#     milestone_id = models.AutoField(primary_key=True)
#     milestone_title = models.CharField(max_length=255)
#     milestone_description = models.TextField()

# class AreasModel(models.Model):
#     """Database model for areas"""
#     IMPORTANCE_LEVEL_CHOICES = [
#         ("high", "High"),
#         ("intermediate", "Intermediate"),
#         ("low", "Low"),
#     ]

#     URGENCY_LEVEL_CHOICES = [
#         ("high", "High"),
#         ("intermediate", "Intermediate"),
#         ("low", "Low"),
#     ]

#     STATUS_CHOICES = [
#         ("to-do", "To-do"),
#         ("doing", "Doing"),
#         ("done", "Done"),
#     ]

#     area_id = models.AutoField(primary_key=True)
#     area_title = models.CharField(max_length=255)
#     area_description = models.TextField(max_length=2000)
#     area_importance_level = models.CharField(choices=IMPORTANCE_LEVEL_CHOICES, max_length=15)
#     area_importance_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
#     area_urgency_level = models.CharField(choices=URGENCY_LEVEL_CHOICES, max_length=15)
#     area_urgency_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
#     area_start = models.DateField()
#     area_end = models.DateField()
#     area_status = models.CharField(choices=STATUS_CHOICES, max_length=10)

#     user = models.ForeignKey(
#         UsersModel,
#         on_delete=models.CASCADE,
#         related_name="areas",
#     )

#     def __str__(self):
#         return f"{self.area_title}"

# class ProjectsModel(models.Model):
#     """Database model for projects"""
#     IMPORTANCE_LEVEL_CHOICES = [
#         ("high", "High"),
#         ("intermediate", "Intermediate"),
#         ("low", "Low"),
#     ]

#     URGENCY_LEVEL_CHOICES = [
#         ("high", "High"),
#         ("intermediate", "Intermediate"),
#         ("low", "Low"),
#     ]

#     STATUS_CHOICES = [
#         ("to-do", "To-do"),
#         ("doing", "Doing"),
#         ("done", "Done"),
#     ]

#     project_id = models.AutoField(primary_key=True)
#     project_title = models.CharField(max_length=255)
#     project_description = models.TextField()
#     project_importance_level = models.CharField(choices=IMPORTANCE_LEVEL_CHOICES, max_length=15)
#     project_importance_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
#     project_urgency_level = models.CharField(choices=URGENCY_LEVEL_CHOICES, max_length=15)
#     project_urgency_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
#     project_deadline = models.DateField()
#     project_start = models.DateField()
#     project_end = models.DateField()
#     project_status = models.CharField(choices=STATUS_CHOICES, max_length=10)


# class SubTasksModel(models.Model):
#     """Database model for sub-tasks"""
#     IMPORTANCE_LEVEL_CHOICES = [
#         ("high", "High"),
#         ("intermediate", "Intermediate"),
#         ("low", "Low"),
#     ]

#     URGENCY_LEVEL_CHOICES = [
#         ("high", "High"),
#         ("intermediate", "Intermediate"),
#         ("low", "Low"),
#     ]

#     STATUS_CHOICES = [
#         ("to-do", "To-do"),
#         ("doing", "Doing"),
#         ("done", "Done"),
#     ]

#     subtask_id = models.AutoField(primary_key=True)
#     subtask_title = models.CharField(max_length=255)
#     subtask_description = models.TextField()
#     subtask_importance_level = models.CharField(choices=IMPORTANCE_LEVEL_CHOICES, max_length=15)
#     subtask_importance_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
#     subtask_urgency_level = models.CharField(choices=URGENCY_LEVEL_CHOICES, max_length=15)
#     subtask_urgency_magnitude = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
#     subtask_deadline = models.DateTimeField()
#     subtask_start = models.DateTimeField()
#     subtask_end = models.DateTimeField()
#     subtask_status = models.CharField(choices=STATUS_CHOICES, max_length=10)
#     # Missing task_tags (under review for normalisation of DB)

# # Junction models (they turn what would be many-to-many relationships to 2 x one-to-many relationships)
# class UsersLifestages(models.Model):
#     """Junction model between users and lifestages"""
#     user = models.ForeignKey(UsersModel, on_delete=models.CASCADE, related_name="user_lifestages")
#     lifestage = models.ForeignKey(LifestagesModel, on_delete=models.PROTECT, related_name="lifestage_users")

# class ResourcesUsers(models.Model):
#     """Junction model between users and resources"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_users")
#     user = models.ForeignKey(UsersModel, on_delete=models.CASCADE, related_name="user_resources")

#     def __str__(self):
#         return f"Resource: {self.resource}, user: {self.user}"

# class ResourcesMilestones(models.Model):
#     """Junction model between resources and milestones"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_milestones")
#     milestone = models.ForeignKey(MilestonesModel, on_delete=models.PROTECT, related_name="milestone_resources")

# class ResourcesTasks(models.Model):
#     """Junction model between resources and tasks"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_tasks")
#     task = models.ForeignKey(TasksModel, on_delete=models.PROTECT, related_name="task_resources")

# class ResourcesAreas(models.Model):
#     """Junction model between resources and areas"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_areas")
#     area = models.ForeignKey(AreasModel, on_delete=models.PROTECT, related_name="area_resources")

# class ResourcesLifestages(models.Model):
#     """Junction model between resources and lifestages"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_lifestages")
#     lifestage = models.ForeignKey(LifestagesModel, on_delete=models.PROTECT, related_name="lifestage_resources")

# class ResourcesProjects(models.Model):
#     """Junction model between resources and projects"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_projects")
#     project = models.ForeignKey(ProjectsModel, on_delete=models.PROTECT, related_name="project_resources")

# class ResourcesSubTasks(models.Model):
#     """Junction model between resources and subtasks"""
#     resource = models.ForeignKey(ResourcesModel, on_delete=models.PROTECT, related_name="resource_subtasks")
#     subtask = models.ForeignKey(SubTasksModel, on_delete=models.PROTECT, related_name="subtask_resources")

# class MilestonesLifestages(models.Model):
#     """Junction model between milestones and lifestages"""
#     milestone = models.ForeignKey(MilestonesModel, on_delete=models.PROTECT, related_name="milestone_lifestages")
#     lifestage = models.ForeignKey(LifestagesModel, on_delete=models.CASCADE, related_name="lifestage_milestones")

# class MilestonesProjects(models.Model):
#     """Junction model between milestones and projects"""
#     milestone = models.ForeignKey(MilestonesModel, on_delete=models.CASCADE, related_name="milestone_projects")
#     project = models.ForeignKey(ProjectsModel, on_delete=models.PROTECT, related_name="project_milestones")

# class MilestonesTasks(models.Model):
#     """Junction model between milestones and tasks"""
#     milestone = models.ForeignKey(MilestonesModel, on_delete=models.CASCADE, related_name="milestone_tasks")
#     task = models.ForeignKey(TasksModel, on_delete=models.PROTECT, related_name="task_milestones")

# class MilestonesSubtasks(models.Model):
#     """Junction model between milestones and subtasks"""
#     milestone = models.ForeignKey(MilestonesModel, on_delete=models.CASCADE, related_name="milestone_subtasks")
#     subtask = models.ForeignKey(SubTasksModel, on_delete=models.PROTECT, related_name="subtask_milestones")

# class LifestagesAreas(models.Model):
#     """Junction model between lifestages and areas"""
#     lifestage = models.ForeignKey(LifestagesModel, on_delete=models.CASCADE, related_name="lifestage_areas")
#     area = models.ForeignKey(AreasModel, on_delete=models.PROTECT, related_name="area_lifestages")
