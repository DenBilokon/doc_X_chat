from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Group, Permission

from django.utils.translation import gettext_lazy as _


class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # document = models.FileField(upload_to='pdf_documents/')
    documentContent = models.TextField(null=True, blank=True)
    embedding = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s PDF: {self.document.name}"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}: Q: {self.question}, A: {self.answer}"


class UserData(models.Model):
    SUBSCRIPTION_CHOICES = (
        ('free', 'Free'),
        ('gold', 'Gold'),
        ('ultra', 'Ultra'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribe_plan = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='free')
    total_files_uploaded = models.IntegerField(default=0)
    total_questions_asked = models.IntegerField(default=0)

    # Обмеження для плану "Free"
    max_files_allowed_free = 5
    max_questions_allowed_free = 20

    # Обмеження для плану "Gold"
    max_files_allowed_gold = 50
    max_questions_allowed_gold = 200

    # Обмеження для плану "Ultra"
    max_files_allowed_ultra = 500
    max_questions_allowed_ultra = 2000

    def max_files_allowed_for_plan(self):
        if self.subscribe_plan == 'free':
            return self.max_files_allowed_free
        elif self.subscribe_plan == 'gold':
            return self.max_files_allowed_gold
        elif self.subscribe_plan == 'ultra':
            return self.max_files_allowed_ultra

    def max_questions_allowed_for_plan(self):
        if self.subscribe_plan == 'free':
            return self.max_questions_allowed_free
        elif self.subscribe_plan == 'gold':
            return self.max_questions_allowed_gold
        elif self.subscribe_plan == 'ultra':
            return self.max_questions_allowed_ultra
