from django.urls import path

from .views import *

app_name = "app_setting_admin"
urlpatterns = [
    # setting
    path(
        "list-create/",
        AdminSettingListCreateAPIView.as_view(),
        name="list_create_setting",
    ),
    path(
        "update/",
        AdminSettingUpdateAPIView.as_view(),
        name="update_setting",
    ),
]
