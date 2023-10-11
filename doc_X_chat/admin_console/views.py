from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

from chat_llm.models import UserData


def is_admin(user):
    """
    The is_admin function checks if the user is authenticated and a superuser.
        
    
    :param user: Check if the user is authenticated and a superuser
    :return: True if the user is authenticated and a superuser
    """
    return user.is_authenticated and user.is_superuser


def get_user_data(user_id):
    """
    The get_user_data function takes a user_id as an argument and returns the UserData object associated with that user.
    If no such object exists, it returns None.
    
    :param user_id: Get the user data for a specific user
    :return: A userdata object or none
    """
    try:
        user_data = UserData.objects.get(user=user_id)
    except UserData.DoesNotExist:
        user_data = None

    return user_data


@user_passes_test(is_admin)
def get_all_users_data(request):
    """
    The get_all_users_data function is responsible for retrieving all users data and rendering it in the admin_console/users_data.html template.
    
    :param request: Get the request object
    :return: A list of dictionaries
    """
    # Ось ваша поточна логіка функції
    current_time = timezone.now()
    users_all_data = User.objects.all()

    # Створюємо список для зберігання даних про всіх користувачів
    users_data = []

    for user in users_all_data:
        user_data = get_user_data(user.id)
        if user.last_login:
            time_since_last_login = current_time - user.last_login
            time_since_last_login = format_duration(time_since_last_login)
        else:
            time_since_last_login = "Never logged in"
        # Створюємо словник із даними користувача
        user_summary = {
            'user': user,
            'user_data': user_data,
            "time_since_last_login": time_since_last_login
        }

        users_data.append(user_summary)

    return render(request, "admin_console/users_data.html", context={'users_data': users_data})


def format_duration(duration):
    """
    The format_duration function takes a timedelta object and returns a string
    representing the duration in days and hours.
    
    
    :param duration: Pass in the timedelta object
    :return: A string that contains the number of days and hours in the duration
    """
    days = duration.days
    hours = duration.seconds // 3600
    return f"{days} days, {hours} hours"
