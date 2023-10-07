from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from cloudinary.exceptions import Error as CloudinaryError

from .forms import RegisterForm, AvatarForm, UpdateUserForm
from .models import Avatar
from chat_llm.models import UserData


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(to='chat_llm:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hello {username}! Your account has been created.")
            return redirect(to="users/signin.html")
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


@login_required
def profile(request):
    """
    The profile function is used to render the profile page of a users.
    """
    user = request.user
    user_id = request.user.id
    user_plan = UserData.objects.get(user=user)
    avatar = Avatar.objects.filter(user_id=user_id).first()
    return render(request, 'users/profile.html',
                  context={'users': user, 'avatar': avatar, 'user_plan': user_plan})


@login_required
def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('users:profile')
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def upload_avatar(request):
    """
    The upload_avatar function allows a users to upload an avatar image.
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    form = AvatarForm()  # Instantiate the form

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                previous_avatar = Avatar.objects.filter(user=request.user).first()
                avatar = form.save(commit=False)
                avatar.user = request.user

                # Validate if the uploaded file is an image
                uploaded_file = form.cleaned_data['image']
                if not uploaded_file.content_type.startswith('image'):
                    raise ValidationError("Invalid file format. Please upload an image.")

                avatar.save()
                if previous_avatar:
                    previous_avatar.delete()

                return redirect('users:profile')
            except (CloudinaryError, ValidationError) as e:
                messages.warning(request, "Invalid file format.")

    return render(request, 'users/user_upload_avatar.html', {'form': form, 'avatar': avatar})


def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect(to='chat_llm:home')


def user_plan_subscription(request):

    user = request.user
    user_plan = UserData.objects.get(user=user)
    return render(request, 'users/user_plan_subscription.html',
                  context={'users': user, 'user_plan': user_plan})
