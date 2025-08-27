from rest_framework import serializers
from .models import Patients

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = fields = ['id', 'name', 'age', 'condition', 'created_at']
        read_only_fields = ['id', 'created_at']

