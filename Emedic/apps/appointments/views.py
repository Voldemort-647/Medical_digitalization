from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Appointment
from .serializer import AppointmentSerializer
from datetime import date
from apps.users.models import doctor, patient


def appointment_dashboard(request):
    return render(request, 'appointments.html')

class AppointmentViewSet(viewsets.ModelViewSet):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """
        optimizes the database query and applies filters for the dashboard.
        """
        queryset = Appointment.objects.all().select_related('patient')
        doctor_id = self.request.query_params.get('doctor_id')
        
        if doctor_id:
            queryset = queryset.filter(
                doctor_id=doctor_id,
                #appointment_date__date=date.today()#
            ).order_by('appointment_date') 
        return queryset