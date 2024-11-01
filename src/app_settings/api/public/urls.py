from django.urls import path

from .views import *

app_name = "app_settings_public"
urlpatterns = [
    # settings
    path(
        "list/",
        UsersSettingsAPIView.as_view(),
        name="list_settings",
    ),
]
