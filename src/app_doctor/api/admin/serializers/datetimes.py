from app_doctor.models import DoctorDateTimeModel

from utils.serializers import CustomModelSerializer


class AdminDoctorDateTimeModelSerializer(CustomModelSerializer):
    class Meta:
        model = DoctorDateTimeModel
        fields = ("id", "doctor", "date", "is_active", "time")
