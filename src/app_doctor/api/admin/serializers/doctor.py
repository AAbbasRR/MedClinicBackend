from app_doctor.models import DoctorModel

from utils.serializers import CustomModelSerializer


class AdminDoctorSerializer(CustomModelSerializer):
    class Meta:
        model = DoctorModel
        fields = (
            "id",
            "name",
            "phone",
            "national_code",
            "address",
            "field",
            "formatted_created_at",
        )
