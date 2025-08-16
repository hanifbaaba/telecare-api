from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        PATIENT = "PATIENT", _("Patient")
        DOCTOR = "DOCTOR", _("Doctor")
        ADMIN = "ADMIN", _("Admin")

    email = models.EmailField(_('email address'), unique = True)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT
    )
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.email
