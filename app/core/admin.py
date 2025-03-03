from django.contrib import admin
from core import models

# Register your models here.
admin.site.register(models.UsersModel)
admin.site.register(models.StoriesModel)
admin.site.register(models.IncidentsModel)
admin.site.register(models.PeoplesModel)
admin.site.register(models.PeopleIncidentModel)
admin.site.register(models.VAKSModel)