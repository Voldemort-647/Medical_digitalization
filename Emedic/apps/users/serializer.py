from rest_framework import serializers
from .models import doctor,patient
class doctorSerializers(serializers.ModelSerializer):
    class Meta():
        model= doctor
        fields='__all__'


class patientSerializer(serializers.ModelSerializer):
    class Meta():
        model = patient
        fields='__all__'

class patientNameserializer(serializers.ModelSerializer):
    class Meta():
        model=patient
        fields=['first_name','last_name']


class doctorNameserializer(serializers.ModelSerializer):
    class Meta():
        model=doctor
        fields=['name','specialization']