from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError, MethodNotAllowed
from .models import Appointment
from .serializers import AppointmentSerializer

User = get_user_model()
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "DOCTOR":
            return Appointment.objects.filter(doctor=user)
        if user.role == "PATIENT":
            return Appointment.objects.filter(patient=user)
        if user.role == "ADMIN":
            return Appointment.objects.all()
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.role not in ["PATIENT", "ADMIN"]:
            raise PermissionDenied("Only patients can create appointments.")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "PATIENT":
            serializer.save(patient=user, status=Appointment.Status.PENDING)
        else:
            patient_id = self.request.data.get("patient")
            if not patient_id:
                raise ValidationError({"patient": "Required when creating as admin."})
            patient = get_object_or_404(User, pk=patient_id, role="PATIENT")
            serializer.save(patient=patient, status=Appointment.Status.PENDING)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    @action(detail=True, methods=["patch"], url_path="approve")
    def approve(self, request, pk=None):
        appt = self.get_object()
        if request.user.role != "DOCTOR" or appt.doctor_id != request.user.id:
            raise PermissionDenied("Only the assigned doctor can approve.")
        if appt.status != Appointment.Status.PENDING:
            raise ValidationError({"status": "Only pending appointments can be approved."})
        appt.status = Appointment.Status.APPROVED
        appt.save(update_fields=["status", "updated_at"])
        return Response(AppointmentSerializer(appt).data)

    @action(detail=True, methods=["patch"], url_path="reject")
    def reject(self, request, pk=None):
        appt = self.get_object()
        if request.user.role != "DOCTOR" or appt.doctor_id != request.user.id:
            raise PermissionDenied("Only the assigned doctor can reject.")
        if appt.status != Appointment.Status.PENDING:
            raise ValidationError({"status": "Only pending appointments can be rejected."})
        appt.status = Appointment.Status.REJECTED
        appt.save(update_fields=["status", "updated_at"])
        return Response(AppointmentSerializer(appt).data)

    @action(detail=True, methods=["patch"], url_path="cancel")
    def cancel(self, request, pk=None):
        appt = self.get_object()
        if request.user.role == "PATIENT":
            if appt.patient_id != request.user.id:
                raise PermissionDenied("You can only cancel your own appointments.")
        elif request.user.role == "ADMIN":
            pass  
        else:
            raise PermissionDenied("Only the patient (or admin) can cancel.")
        if appt.status not in [Appointment.Status.PENDING, Appointment.Status.APPROVED]:
            raise ValidationError({"status": "Only pending/approved appointments can be cancelled."})
        appt.status = Appointment.Status.CANCELLED
        appt.save(update_fields=["status", "updated_at"])
        return Response(AppointmentSerializer(appt).data)
