from django.db import models

# Create your models here.
class doctor(models.Model):
    name=models.CharField(max_length=255)
    specialization=models.CharField(max_length=40)
    license_no=models.IntegerField()
    phone_no=models.CharField(max_length=12)


class patient(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    blood_type=models.CharField(max_length=4)
    gender=models.CharField(max_length=1)
    dob=models.DateTimeField()
    phone=models.CharField(max_length=12)