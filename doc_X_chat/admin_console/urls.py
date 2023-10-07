from django.urls import path


from .views import get_all_users_data

app_name = "admin_console"

urlpatterns = [
    path('users_data/', get_all_users_data, name='users_data'),
    ]
