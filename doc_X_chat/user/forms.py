from django import forms
from .models import CustomProfile


class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    Allows users to input their phone number and address when registering.

    :param forms.ModelForm: Model form for user registration.
    """

    class Meta:
        model = CustomProfile
        fields = ('phone', 'address')
