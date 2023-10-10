from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserData


@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwargs):
    """
    The create_user_data function is a signal that creates an instance of the UserData model
        when a new user is created. The function takes four arguments: sender, instance, created and kwargs.
        The sender argument refers to the model class that sends the signal (User). 
        The instance argument refers to the actual instance being saved (the user object). 
        Created indicates whether or not this is a new record being saved to the database for 
            the first time or if it’s an existing record being updated. Kwargs contains any keyword arguments.
    
    :param sender: Specify the model that is being sent to the function
    :param instance: Get the user object
    :param created: Check if the user is created or not
    :param **kwargs: Pass in any additional keyword arguments
    :return: A userdata object
    """
    if created:
        UserData.objects.create(user=instance, subscribe_plan='free')
