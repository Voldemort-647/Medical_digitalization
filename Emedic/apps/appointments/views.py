from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Appointment
from apps.users.models import patient,doctor
from rest_framework.decorators import action,api_view
from rest_framework.response import Response
from django.utils import timezone
from .serializer import AppointmentSerializer
from apps.users.serializer import patientNameserializer


# Create your views here.
@api_view(['POST'])
def add(request):
    inpuData=AppointmentSerializer(data=request.data)
    if inpuData.is_valid():
        inpuData.save()
    return Response(inpuData.data)
@api_view(['GET'])
def patientHistory(request,pk):
    Patient=get_object_or_404(patient,id=pk)
    Pjson=patientNameserializer(Patient).data
    History=Appointment.objects.filter(patient_id=pk)
    listOfApp=[]
    for singular in History:
        temp_var=AppointmentSerializer(singular).data
        listOfApp.append(temp_var)
    Pjson["appt"]=listOfApp
    return Response(Pjson)

@api_view(['GET'])
def display(request):
    appointments=Appointment.objects.all()
    json=AppointmentSerializer(appointments,many=True)
    return Response(json.data)


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