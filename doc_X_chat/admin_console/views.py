from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

from chat_llm.models import UserData


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def get_user_data(user_id):
    try:
        user_data = UserData.objects.get(user=user_id)
    except UserData.DoesNotExist:
        user_data = None

    return user_data


@user_passes_test(is_admin)
def get_all_users_data(request):
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
    days = duration.days
    hours = duration.seconds // 3600
    return f"{days} days, {hours} hours"
