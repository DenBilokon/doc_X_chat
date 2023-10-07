from django.contrib import admin
from .models import PDFDocument, ChatMessage
from .models import CustomProfile, PDFDocument, ChatMessage

# Register your models here.
admin.site.register(CustomProfile)
admin.site.register(PDFDocument)
admin.site.register(ChatMessage)
