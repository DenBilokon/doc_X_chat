from django.core.exceptions import ValidationError
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from cloudinary.exceptions import Error as CloudinaryError

from .forms import RegisterForm, AvatarForm, UpdateUserForm
from .models import Avatar
from chat_llm.models import UserData

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str


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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Check if a user with this username already exists
            if get_user_model().objects.filter(username=username).exists():
                form.add_error('username', ValidationError('This username is already taken.'))
                return render(request, self.template_name, {'form': form})

            # Check if a user with this email already exists
            if get_user_model().objects.filter(email=email).exists():
                form.add_error('email', ValidationError('This email is already in use.'))
                return render(request, self.template_name, {'form': form})

            user = form.save(commit=False)
            user.is_active = False
            user.save()  # Зберігаємо користувача у базу даних

            # Generate email confirmation token and url
            token = default_token_generator.make_token(user)

            # Отримуємо uid після збереження користувача
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Get current site domain
            # !!!!!!!!!!!!!!! додати домен !!!!!!!!!!!!!!!!!!!
            # domain = get_current_site(request).domain

            # Prepare email text
            mail_subject = 'Activate your account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': uid,
                'token': token,
            })

            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            messages.success(request,
                             f"Hello {user.username}! Your account has been created. Please check your email to "
                             f"confirm your account.")
            return redirect(to="users:login")
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


def activate_account(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/account_activation_done.html')
        else:
            return render(request, 'users/account_activation_invalid.html')
    except Exception as ex:
        pass

    return redirect(to="users:login")
