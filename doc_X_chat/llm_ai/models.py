from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # document = models.FileField(upload_to='pdf_documents/')
    documentContent = models.TextField(null=True, blank=True)
    embedding = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s PDF: {self.document.name}"
