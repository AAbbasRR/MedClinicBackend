from app_doctor.models import DoctorModel

from utils.serializers import CustomModelSerializer


class UsersDoctorSerializer(CustomModelSerializer):
    class Meta:
        model = DoctorModel
        fields = (
            "id",
            "name",
            "field",
        )
