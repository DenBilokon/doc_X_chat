from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ClearableFileInput

from .models import Avatar


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput({'class': 'form-control',
                                                       'placeholder': 'username'}))
    email = forms.CharField(max_length=50, required=True,
                            widget=forms.EmailInput({'class': 'form-control',
                                                     'placeholder': 'username@gmail.com'}))
    first_name = forms.CharField(max_length=50, required=True,
                                 widget=forms.TextInput({'class': 'form-control',
                                                         'placeholder': 'first_name'}))
    last_name = forms.CharField(max_length=50, required=False,
                                widget=forms.TextInput({'class': 'form-control',
                                                        'placeholder': 'last_name'}))
    password1 = forms.CharField(max_length=50, min_length=5, required=True,
                                widget=forms.PasswordInput({'class': 'form-control',
                                                            'placeholder': 'password1'}))
    password2 = forms.CharField(max_length=50, min_length=5, required=True,
                                widget=forms.PasswordInput({'class': 'form-control',
                                                            'placeholder': 'password2'}))



    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=50, required=True,
#                                widget=forms.TextInput({'class': 'form-control',
#                                                        'placeholder': 'username'}))
#     password = forms.CharField(max_length=50, min_length=5, required=True,
#                                widget=forms.PasswordInput({'class': 'form-control',
#                                                            'placeholder': 'password'}))
#
#     class Meta:
#         model = User
#         fields = ["username", "password"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput({'class': 'form-control',
                                                       'placeholder': 'username'}))
    password = forms.CharField(max_length=50, min_length=5, required=True,
                               widget=forms.PasswordInput({'class': 'form-control',
                                                           'placeholder': 'password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Перевірка чи користувач існує і чи пароль вірний
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Невірне ім'я користувача або пароль.")

        return cleaned_data


class AvatarForm(ModelForm):
    class Meta:
        model = Avatar
        fields = ['image', ]
        widgets = {'image': ClearableFileInput(attrs={'class': 'form-control-file'})}


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class UserPlanForm(forms.ModelForm):
    pass


