from django.contrib import admin
from django.urls import path, include
from . import views, pdfChat
from llmApp.views import *
from llmApp.pdfChat import *

urlpatterns = [
    path('', views.home, name='home'),
]