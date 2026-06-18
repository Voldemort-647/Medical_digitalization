from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Appointment
from apps.users.models import patient,doctor
from rest_framework.decorators import action,api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Appointment
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