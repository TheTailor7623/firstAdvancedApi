from django.contrib import admin
from core import models

# Users
admin.site.register(models.UsersModel)
# Stories
admin.site.register(models.StoriesModel)
# Incident
admin.site.register(models.IncidentsModel)
# People
admin.site.register(models.PeoplesModel)
# VAKS
admin.site.register(models.VAKSModel)
# Points
admin.site.register(models.PointsModel)
# Links
admin.site.register(models.LinksModel)
# Junction tables
admin.site.register(models.StoryLinkModel)
admin.site.register(models.PeopleIncidentModel)