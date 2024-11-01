from rest_framework import serializers

from app_settings.models import SettingsModel

from utils.serializers import CustomModelSerializer


class AdminSettingsSerializer(CustomModelSerializer):
    class Meta:
        model = SettingsModel
        fields = (
            "id",
            "value",
            "type",
        )
