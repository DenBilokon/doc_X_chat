from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name='home'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf')
]
