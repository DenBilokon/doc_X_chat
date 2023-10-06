from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone


# # Create your models here.
# class CustomProfile(models.Model):
#     users = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15)
#     address = models.CharField(max_length=100)
#
#
#     def __str__(self):
#         return self.users.username


EXTENSIONS_IMG = ['jpeg', 'png', 'jpg', 'svg', 'gif']


class Avatar(models.Model):
    image = CloudinaryField(resource_type='auto', allowed_formats=EXTENSIONS_IMG, folder='avatars doc_X_chat')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
