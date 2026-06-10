from django.db import models
from app.users.models import patient,doctor

# Create your models here.
class Medicine(models.Model):
    medicine_name = models.CharField(max_length=255),
    power - models.CharField(max_length=30),
    active_ing = models.BooleanField(),
    generic_use = models.CharField(max_length=255)
    def __str__(self):
        return self.medicine_name
    

class Prescription(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Expired", "Expired"),
        ("Cancelled", "Cancelled")
    ]   

    patient = models.ForeignKey(patient,on_delete=models.CASCADE)
    doctor =  models.ForeignKey(doctor,on_delete=models.CASCADE)
    prescribed_date = models.DateField(auto_now_add=True)
    diagnosis_notes = models.TextField()
    doctor_notes = models.TextField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="UNKNOWN")

    def __str__(self):
        return (f"Prescription for {self.pk}")   
    

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.PROTECT)
    dosage_frequency = models.CharField(max_length=100)
    duration = models.DATETimeField()

    def __str__(self):
        return f"{self.medicine.medicine_name} for {self.prescription.patient.first_name}"