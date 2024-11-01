from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static

v1_user_urlpatterns = [
    path(
        "auth/",
        include("app_user.api.user.urls", namespace="app_user_auth"),
    ),
    path(
        "doctor/",
        include("app_doctor.api.public.urls", namespace="app_doctor_public"),
    ),
    path(
        "settings/",
        include("app_settings.api.public.urls", namespace="app_settings_public"),
    ),
    path(
        "reservations/",
        include("app_reservation.api.public.urls", namespace="app_reservation_public"),
    ),
]

v1_admin_urlpatterns = [
    path(
        "user/",
        include("app_user.api.manager.urls", namespace="app_user_manager"),
    ),
    path(
        "doctor/",
        include("app_doctor.api.admin.urls", namespace="app_doctor_admin"),
    ),
    path(
        "reservations/",
        include("app_reservation.api.admin.urls", namespace="app_reservation_admin"),
    ),
    path(
        "settings/",
        include("app_settings.api.admin.urls", namespace="app_setting_admin"),
    ),
]
v1_urlpatterns = [
    path("public/", include(v1_user_urlpatterns)),
    path("admin/", include(v1_admin_urlpatterns)),
]

urlpatterns = [
    path("api/<str:version>/", include(v1_urlpatterns)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = "utils.url_handlers.custom_404_response"
handler500 = "utils.url_handlers.custom_500_response"
