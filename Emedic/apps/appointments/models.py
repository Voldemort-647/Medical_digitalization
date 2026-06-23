from django.db import models
from apps.users.models import patient,doctor

# Create your models here.
class Appointment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled")
    ]

    patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctor, on_delete = models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    appointment_time = models.TimeField()

    class Meta:
     constraints = [
        models.UniqueConstraint(
             fields=[
                    "doctor",
                   "appointment_date",
                  "appointment_time"
              ],
              name="unique_doctor_slot"
    )
    ]

def __str__(self):
        return f"Appointment q- {self.patient.first_name} with Dr. {self.doctor.first_name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"