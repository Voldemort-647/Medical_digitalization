from rest_framework import serializers
from .models import doctor,patient
from datetime import date
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

class patientAppointmentserializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta():
        model=patient
        fields=['first_name','last_name','age','gender']

    def get_age(self, obj):
    # 1. Grab the dob value from the model instance
        dob_field = getattr(obj, 'dob', None)
        
        if not dob_field:
            return None
            
        try:
            # 2. Extract ONLY the date portion, dropping the time stamp safely
            # works perfectly if dob_field is a datetime object or a standard date object
            dob = dob_field.date() if hasattr(dob_field, 'date') else dob_field
            
            today = date.today()
            
            # 3. Dynamic age calculation with birthday boundary correction
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return age
        except Exception as e:
            return None