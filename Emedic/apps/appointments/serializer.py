from rest_framework import serializers
from .models import Appointment
from apps.users.serializer import patientNameserializer

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Appointment
        fields='__all__'

class dashboardSerializer(serializers.ModelSerializer):
    pt=patientNameserializer(source='patient')
    class Meta():
        model=Appointment
        fields=['pt','appointment_date','appointment_time','status','reason']