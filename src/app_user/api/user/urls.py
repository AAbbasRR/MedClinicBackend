from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

app_name = "app_user_auth"
urlpatterns = [
    # login
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_token_refresh"),
    # info
    path("info/", UserInfoAPIView.as_view(), name="info_account"),
    # change password
    path(
        "change_password/",
        UserChangePasswordAPIView.as_view(),
        name="change_password",
    ),
]
