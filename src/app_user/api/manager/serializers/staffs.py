from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app_user.models import UserModel

from utils.serializers import CustomModelSerializer


class ManagerUserStaffsSerializer(CustomModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )

    class Meta:
        model = UserModel
        fields = (
            "id",
            "first_name",
            "last_name",
            "is_staff",
            "email",
            "password",
            "formatted_last_login",
            "formatted_date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.method.upper() in ["PUT", "PATCH"]:
            self.fields["email"].validators = []

    def create(self, validated_data):
        validated_data["is_staff"] = True
        validated_data["is_superuser"] = False
        return UserModel.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance
