from django.db import models
from django.conf import settings
# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
