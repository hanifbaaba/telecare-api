from django.db import models
from django.conf import settings

# Create your models here.
class Patients(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    condition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, blank=True, null=True)



    def __str__(self):
        return self.name
    