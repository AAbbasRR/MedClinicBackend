from app_settings.models import SettingsModel

from utils.serializers import CustomModelSerializer


class UsersSettingsSerializer(CustomModelSerializer):
    class Meta:
        model = SettingsModel
        fields = (
            "id",
            "type",
            "value",
        )
