from django.urls import path
from . import views



urlpatterns = [
    path('', views.main, name='home'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('ask_question/', views.ask_question, name='ask_question'),
    path('get_chat_history/', views.get_chat_history, name='get_chat_history'),
]
