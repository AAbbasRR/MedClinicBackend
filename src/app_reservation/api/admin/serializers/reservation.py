from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from import_export import resources, fields

from app_reservation.models import ReservationModel

from utils.serializers import CustomModelSerializer


class AdminReservationSerializer(CustomModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = ReservationModel
        fields = (
            "id",
            "doctor",
            "year",
            "month",
            "date",
            "day_of_week",
            "time",
            "first_name",
            "last_name",
            "mobile_number",
            "national_code",
        )

    def get_doctor(self, obj):
        return {
            "name": obj.doctor.name,
            "field": obj.doctor.field,
        }


class AdminReservationExportResource(resources.ModelResource):
    doctor = fields.Field(column_name=_("doctor"))
    date = fields.Field(column_name=_("date"))
    day_of_week = fields.Field(column_name=_("day_of_week"))
    time = fields.Field(column_name=_("time"))
    first_name = fields.Field(column_name=_("first_name"))
    last_name = fields.Field(column_name=_("last_name"))
    national_code = fields.Field(column_name=_("national_code"))
    mobile_number = fields.Field(column_name=_("mobile_number"))

    class Meta:
        model = ReservationModel
        fields = (
            "doctor",
            "date",
            "day_of_week",
            "time",
            "first_name",
            "last_name",
            "national_code",
            "mobile_number",
        )

    def dehydrate_doctor(self, obj):
        return f"{obj.doctor.name}({obj.doctor.field})"

    def dehydrate_date(self, obj):
        return f"{obj.year}-{obj.month}-{obj.date}"

    def dehydrate_day_of_week(self, obj):
        return obj.day_of_week

    def dehydrate_time(self, obj):
        return obj.time

    def dehydrate_first_name(self, obj):
        return obj.first_name

    def dehydrate_last_name(self, obj):
        return obj.last_name

    def dehydrate_national_code(self, obj):
        return obj.national_code

    def dehydrate_mobile_number(self, obj):
        return obj.mobile_number
