from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import doctorSerializers,patientSerializer
from rest_framework.decorators import api_view
from .models import doctor,patient
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

def hello(request):
    return HttpResponse("hello this is my project")