from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from import_export import resources, fields

from app_reservation.models import ReservationModel

from utils.serializers import CustomModelSerializer

import jdatetime


class AdminReservationSerializer(CustomModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = ReservationModel
        fields = (
            "id",
            "doctor",
            "date",
            "time",
            "full_name",
            "mobile_number",
        )

    def get_doctor(self, obj):
        return {
            "name": obj.doctor.name,
            "field": obj.doctor.field,
        }


class AdminCreateReservationSerializer(CustomModelSerializer):
    class Meta:
        model = ReservationModel
        fields = (
            "id",
            "doctor",
            "date",
            "time",
            "full_name",
            "mobile_number",
        )


class AdminReservationExportResource(resources.ModelResource):
    doctor = fields.Field(column_name=_("doctor"))
    date = fields.Field(column_name=_("date"))
    time = fields.Field(column_name=_("time"))
    full_name = fields.Field(column_name=_("full_name"))
    mobile_number = fields.Field(column_name=_("mobile_number"))

    class Meta:
        model = ReservationModel
        fields = (
            "doctor",
            "date",
            "time",
            "full_name",
            "mobile_number",
        )

    def dehydrate_doctor(self, obj):
        return f"{obj.doctor.name}({obj.doctor.field})"

    def dehydrate_date(self, obj):
        year, month, day = map(int, str(obj.date).split("-"))
        jalali_date = jdatetime.GregorianToJalali(year, month, day)
        return f"{jalali_date.jyear}/{jalali_date.jmonth}/{jalali_date.jday}"

    def dehydrate_time(self, obj):
        return obj.time

    def dehydrate_full_name(self, obj):
        return obj.full_name

    def dehydrate_mobile_number(self, obj):
        return obj.mobile_number
