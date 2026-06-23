from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import render,get_object_or_404, redirect
from .models import Appointment
from django.contrib import messages
from django.db import IntegrityError
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
        queryset = Appointment.objects.all().select_related('patient').filter(status = "Scheduled")
        doctor_id = self.request.query_params.get('doctor_id')
        
        if doctor_id:
            queryset = queryset.filter(
                doctor_id=doctor_id,
                #appointment_date__date=date.today()#
            ).order_by('appointment_date') 
        return queryset
    
def patientbooking(request, doctor_id):
    doctor_obj = get_object_or_404(doctor,pk=doctor_id)
    return render( request,'patient_booking.html', {'doctor': doctor_obj})


class BookingViewSet(viewsets.ViewSet):

    @transaction.atomic
    def create(self, request, doctor_id):
        doctor_obj = get_object_or_404(doctor, pk=doctor_id)
        # 1. Create patient
        patient_obj, created = patient.objects.get_or_create(
            phone=request.data.get("phone"),
            defaults={
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "blood_type": request.data.get("blood_type"),
                "gender": request.data.get("gender"),
                "dob": request.data.get("dob")
            }
        )
        # 2. Create appointment
        appointment_data = {
            "patient": patient_obj.id,
            "doctor": doctor_obj.id,
            "appointment_date": request.data.get("appointment_date"),
            "appointment_time": request.data.get("appointment_time"),
            "reason": request.data.get("reason")
        }
        serializer = AppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            serializer.save(status = "Pending")
            return Response(serializer.data,status=201)

        return Response(
            serializer.errors,
            status=400
        )
    

def receptionist_dashboard(request):
    pending_appointments = (
        Appointment.objects
        .select_related("patient")
        .filter(status="Pending")
        .order_by("appointment_date")
        )

    return render(request,"receptionist.html", {"pending_appointments": pending_appointments})
    
def update_appointment_status(request,appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment,id=appointment_id)
        new_time = request.POST.get("appointment_time")
        conflict = Appointment.objects.filter(doctor=appointment.doctor, appointment_date=appointment.appointment_date, appointment_time=new_time, status="Scheduled"
        ).exclude(id=appointment.id).exists()

        if conflict:
            messages.error(request,"Time slot already occupied." )
            return redirect("receptionist_dashboard")
        appointment.appointment_time = new_time
        appointment.status = "Scheduled"
        appointment.save()
        messages.success(request, "Appointment scheduled.")
        return redirect("receptionist_dashboard")

        try:
            appointment.appointment_time = new_time
            appointment.status = "Scheduled"
            appointment.save()
            messages.success(request,"Appointment scheduled.")

        except IntegrityError:
            messages.error(request, "This slot is already occupied.")
    return redirect("receptionist_dashboard")        
    