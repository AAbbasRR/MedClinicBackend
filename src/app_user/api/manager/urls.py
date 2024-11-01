from django.urls import path

from .views import *

app_name = "app_user_manager"
urlpatterns = [
    # staffs
    path(
        "staffs/list-create/",
        ManagerUserStaffsListCreateAPIView.as_view(),
        name="list_create_user_staffs",
    ),
    path(
        "staffs/update-delete/",
        ManagerUserStaffsUpdateDeleteAPIView.as_view(),
        name="update_delete_user_staffs",
    ),
]
