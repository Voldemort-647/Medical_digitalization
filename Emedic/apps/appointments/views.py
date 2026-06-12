from rest_framework import viewsets
from .models import Appointment
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .serializer import AppointmentSerializer


# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(detail = False)
    def today(self,request):
        today = timezone.now().date()
        appointments = self.queryset.filter(appointment_date__date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail = False)
    def doctor_queue(self,request):
        doctorr = request.user.doctor
        today = timezone.now().date()
        appointments = self.queryset.filter(doctor=doctorr, appointment_date__date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)