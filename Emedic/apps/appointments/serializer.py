from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Appointment
        fields='__all__'

class dashboardSerializer(serializers.ModelSerializer):
    class Meta():
        model=Appointment
        fields=['appointment_date','appointment_time','status','reason']