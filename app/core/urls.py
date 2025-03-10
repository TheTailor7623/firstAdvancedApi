from django.urls import path, include
from core import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Dashboard endpoints
    path("", views.dashboardApi.as_view(), name="dashboard-endpoint"),
    # User endpoints
    path("user/", views.userProfileApi.as_view(), name="user-profile-endpoint"),
    path("user/registration/", views.registerUserApi.as_view(), name="user-registration-endpoint"),
    # Authentication endpoints
    path("user/token/", TokenObtainPairView.as_view(), name="token-obtain-pair-endpoint"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token-refresh-endpoint"),
    # Story endpoints
    path("stories/", views.storiesApi.as_view(), name="stories"),
    path("stories/create-new-story/", views.storyCreateApi.as_view(), name="create-story"),
    path("stories/<int:story_id>/", views.storyDetailsApi.as_view(), name="story-details"),
    # Incident endpoint
    path("stories/<int:story_id>/incident/", views.storyIncidentApi.as_view(), name="story-incident"),
    # People endpoints
    path("stories/<int:story_id>/people/", views.storyPeopleApi.as_view(), name="story-people"),
    path("stories/<int:story_id>/people/<int:person_id>/", views.storyPeopleApiDetails.as_view(), name="story-people-details"),
    # VAKS endpoints
    path("stories/<int:story_id>/vaks/", views.vaksApi.as_view(), name="story-vaks"),
    # Point endpoints
    path("stories/<int:story_id>/points/", views.pointsApi.as_view(), name="story-points"),
    path("stories/<int:story_id>/points/<int:point_id>/", views.pointDetailsApi.as_view(), name="story-point-details"),
    # Script endpoints
    path("stories/<int:story_id>/script/", views.scriptApi.as_view(), name="story-script"),
    # Link endpoints
    path("stories/<int:story_id>/links/", views.linksApi.as_view(), name="story-links"),
    path("stories/<int:story_id>/links/<int:link_id>/", views.linkDetailsApi.as_view(), name="story-link-details"),
    # Character endpoints
    path("stories/<int:story_id>/characters/", views.charactersApi.as_view(), name="story-characters"),
    path("stories/<int:story_id>/characters/<int:character_id>/", views.characterDetailsApi.as_view(), name="story-character-details"),
]
