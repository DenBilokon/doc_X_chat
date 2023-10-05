from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username
