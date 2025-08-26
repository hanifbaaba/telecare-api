from django.db import models
from django.conf import settings

# Create your models here.
class Prescriptions(models.Model):
      doctor = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, 
            related_name='prescriptions_given'
            )
      patient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='prescriptions_received'
            )
      medication = models.CharField(max_length=200)
      dosage = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
 
      def __str__(self):
        return f"Prescription by {self.doctor} for {self.patient}"