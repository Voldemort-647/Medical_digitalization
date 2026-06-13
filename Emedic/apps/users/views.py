from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# from django.views import View
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import doctorSerializers,patientSerializer,patientNameserializer
from rest_framework.decorators import api_view
from .models import doctor,patient
from apps.appointments.serializer import dashboardSerializer
from apps.appointments.models import Appointment
# Create your views here.



@api_view(['POST'])
def add_data(request):
    datad=patientSerializer(data=request.data)
    if datad.is_valid():
        datad.save()
    return Response(datad.data)




@api_view(['GET'])
def display_data(request):
    info= patient.objects.all()
    datad=patientSerializer(info,many=True)
    return Response(datad.data)






@api_view(['PUT'])
def modify_data(request,pk):   
    info = patient.objects.get(pk=pk)
    serializer=patientSerializer(info,data =request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)





@api_view(['GET'])
def dshbrd(request,pk):
   tr_doctor=get_object_or_404(doctor,id=pk)
  # dr_json=doctorSerializers(tr_doctor).data
   appointment= Appointment.objects.filter(doctor_id=pk).select_related('patient')
   data_store=[]
   for singular in appointment:
       temp_var= dashboardSerializer(singular).data
       temp_var['pt']=patientNameserializer(singular.patient).data

       data_store.append(temp_var)
   return Response(data_store)





def hello(request):
    return HttpResponse("hello this is my project")