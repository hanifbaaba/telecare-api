from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Appointment

User = get_user_model()
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "scheduled_for",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "patient", "status", "created_at", "updated_at"]

    def validate(self, attrs):
        doctor = attrs.get("doctor")
        scheduled_for = attrs.get("scheduled_for")

        if not doctor:
            raise serializers.ValidationError({"doctor": "This field is required."})
        if getattr(doctor, "role", None) != "DOCTOR":
            raise serializers.ValidationError({"doctor": "Selected user is not a doctor."})
        if not scheduled_for:
            raise serializers.ValidationError({"scheduled_for": "This field is required."})
        if scheduled_for <= timezone.now():
            raise serializers.ValidationError({"scheduled_for": "Must be in the future."})

        exists = Appointment.objects.filter(
            doctor=doctor,
            scheduled_for=scheduled_for,
            status__in=[Appointment.Status.PENDING, Appointment.Status.APPROVED],
        ).exists()
        if exists:
            raise serializers.ValidationError(
                {"scheduled_for": "Doctor is not available at this time."}
            )

        return attrs
