from rest_framework import serializers
from .models import Appointment, patient, doctor
from apps.users.serializer import patientAppointmentserializer,doctorNameserializer
from django.utils import timezone

class AppointmentSerializer(serializers.ModelSerializer):
    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value
    pt = patientAppointmentserializer(source = "patient", read_only=True)
    dt = doctorNameserializer(source = "doctor",read_only = True)

    patient = serializers.PrimaryKeyRelatedField(queryset=patient.objects.all(), write_only = True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=doctor.objects.all(), write_only = True)


    class Meta():
        model = Appointment
        fields='__all__'

class dashboardSerializer(serializers.ModelSerializer):
    class Meta():
        model=Appointment
        fields=['appointment_date','appointment_time','status','reason']

class ReceptionistSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    phone = serializers.CharField(source="patient.phone", read_only=True)
    class Meta:
        model = Appointment
        fields = ["id", "patient_name", "phone", "appointment_date", "reason"]

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"