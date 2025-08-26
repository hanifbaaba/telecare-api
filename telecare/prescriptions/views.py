from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Prescriptions
from .serializers import PrescriptionsSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class PrescriptionViewSet(viewsets.ModelViewSet):
    # queryset = Doctors.objects.all()
    serializer_class = PrescriptionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "DOCTOR":
            return Prescriptions.objects.filter(doctor=user)
        elif user.role == "PATIENT":
            return Prescriptions.objects.filter(patient=user)
        elif user.role == "ADMIN":
            return Prescriptions.objects.all()
        return Prescriptions.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role != "DOCTOR":
            raise PermissionDenied("Only doctors can create prescriptions.")
        serializer.save(doctor=self.request.user)
