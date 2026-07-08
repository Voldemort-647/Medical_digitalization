from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, IntegrityError
from django.contrib import messages
from datetime import date

from .models import Appointment
from .serializer import AppointmentSerializer
from apps.users.models import patient, doctor
from apps.users.serializer import patientNameserializer


# Utility API endpoints
@api_view(['POST'])
def add(request):
    """Create a new appointment via POST request."""
    input_data = AppointmentSerializer(data=request.data)
    if input_data.is_valid():
        input_data.save()
    return Response(input_data.data)


@api_view(['GET'])
def patientHistory(request, pk):
    """Retrieve complete appointment history for a specific patient."""
    patient_obj = get_object_or_404(patient, id=pk)
    patient_json = patientNameserializer(patient_obj).data
    
    history = Appointment.objects.filter(patient_id=pk)
    appointments_list = [AppointmentSerializer(appt).data for appt in history]
    
    patient_json["appt"] = appointments_list
    return Response(patient_json)


@api_view(['GET'])
def display(request):
    """Display all appointments in the system."""
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Page views
def appointment_dashboard(request):
    """Render the appointment dashboard template."""
    return render(request, 'appointments.html')


def patientbooking(request, doctor_id):
    """Render patient booking page for a specific doctor."""
    doctor_obj = get_object_or_404(doctor, pk=doctor_id)
    return render(request, 'patient_booking.html', {'doctor': doctor_obj})


def receptionist_dashboard(request):
    """Display pending appointments for receptionist approval."""
    pending_appointments = (
        Appointment.objects
        .select_related("patient")
        .filter(status="Pending")
        .order_by("appointment_date")
    )
    return render(request, "receptionist.html", {"pending_appointments": pending_appointments})


def update_appointment_status(request, appointment_id):
    """Approve and schedule a pending appointment."""
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        new_time = request.POST.get("appointment_time")
        
        # Check for time slot conflicts
        conflict = Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=appointment.appointment_date,
            appointment_time=new_time,
            status="Scheduled"
        ).exclude(id=appointment.id).exists()

        if conflict:
            messages.error(request, "Time slot already occupied.")
            return redirect("receptionist_dashboard")
        
        # Update appointment status
        appointment.appointment_time = new_time
        appointment.status = "Scheduled"
        appointment.save()
        messages.success(request, "Appointment scheduled.")
    
    return redirect("receptionist_dashboard")


# ViewSets
class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing appointments with filtering and optimization."""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """Optimize database queries and apply filters for the dashboard."""
        queryset = Appointment.objects.all().select_related('patient').filter(status="Scheduled")
        doctor_id = self.request.query_params.get('doctor_id')
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id).order_by('appointment_date')
        
        return queryset


class BookingViewSet(viewsets.ViewSet):
    """ViewSet for handling patient appointment bookings."""
    
    @transaction.atomic
    def create(self, request, doctor_id):
        """Create a new appointment and patient record if needed."""
        doctor_obj = get_object_or_404(doctor, pk=doctor_id)
        
        # Get or create patient
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
        
        # Create appointment
        appointment_data = {
            "patient": patient_obj.id,
            "doctor": doctor_obj.id,
            "appointment_date": request.data.get("appointment_date"),
            "appointment_time": request.data.get("appointment_time"),
            "reason": request.data.get("reason")
        }
        serializer = AppointmentSerializer(data=appointment_data)
        
        if serializer.is_valid():
            serializer.save(status="Pending")
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# Class-based views (if defined in your views)
class AppointmentsToday(viewsets.ViewSet):
    """ViewSet for today's appointments."""
    pass


class AppoinmentsByDoctor(viewsets.ViewSet):
    """ViewSet for appointments filtered by doctor."""
    pass


class AppointmentsCreate(viewsets.ViewSet):
    """ViewSet for creating appointments."""
    pass


class AppointmentsDetail(viewsets.ViewSet):
    """ViewSet for appointment details."""
    pass


class AppointmentsUpdate(viewsets.ViewSet):
    """ViewSet for updating appointments."""
    pass


class AppointmentCancel(viewsets.ViewSet):
    """ViewSet for cancelling appointments."""
    pass
