from django.shortcuts import render
from rest_framework import viewsets, permissions,  generics
from .models import Patients
from .serializers import PatientSerializer
# from rest_framework import generics, permissions
from prescriptions.serializers import PrescriptionsSerializer
from prescriptions.models import Prescriptions

class PatientViewSet(viewsets.ModelViewSet):
    # queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "ADMIN":
           return Patients.objects.all()
        return Patients.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

