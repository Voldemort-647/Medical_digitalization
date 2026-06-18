from rest_framework import serializers
from .models import Appointment
from apps.users.serializer import patientAppointmentserializer,doctorNameserializer

class AppointmentSerializer(serializers.ModelSerializer):
    pt = patientAppointmentserializer(source = "patient", read_only=True)
    dt = doctorNameserializer(source = "doctor",read_only = True)

    
    class Meta():
        model = Appointment
        fields='__all__'

class dashboardSerializer(serializers.ModelSerializer):
    class Meta():
        model=Appointment
        fields=['appointment_date','appointment_time','status','reason']