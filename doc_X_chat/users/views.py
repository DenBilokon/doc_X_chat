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
            password1 = form.cleaned_data.get('password1')

            if len(username) < 5:
                form.add_error('username', ValidationError("Username must be at least 5 characters long."))
            if len(password1) < 8:
                form.add_error('password1', ValidationError("Password must be at least 8 characters long."))

            if form.errors:
                return render(request, self.template_name, {'form': form})

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
                'domain': "127.0.0.1",
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


def activate_account(request, uid, token):
    """
    The activate_account function is responsible for activating a user's account.
        It takes in two parameters: request and uidb64, token. The request parameter is the HTTP GET Request object that contains information about the current HTTP request.
        The uidb64 parameter is a string representation of an integer that has been base 64 encoded to protect it from being tampered with by malicious users who may try to change its value in order to activate another user's account instead of their own.
    
    :param request: Get the request object
    :param uid: Decode the uidb64 value in the url
    :param token: Check if the user is valid
    :return: A render() function, which is a httpresponse object
    """
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


@login_required
def profile(request):
    """
    The profile function is used to render the profile page of a users.
    
    :param request: Get the current user
    :return: The user, avatar and user_plan
    """
    user = request.user
    user_id = request.user.id
    user_plan = UserData.objects.get(user=user)
    avatar = Avatar.objects.filter(user_id=user_id).first()
    return render(request, 'users/profile.html',
                  context={'users': user,
                           'avatar': avatar,
                           'user_plan': user_plan})


@login_required
def update_user(request):
    """
    The update_user function is used to update the user's profile.
        The function takes in a request and returns a render of the users/profile.html page with an UpdateUserForm instance.
    
    :param request: Get the current user
    :return: A render method that renders the profile page with the form
    """
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
    
    :param request: Get the request object, which contains information about the current web request
    :return: A render function that renders the user_upload_avatar.html page with the form and avatar
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

    return render(request, 'users/user_upload_avatar.html', {'form': form,
                                                             'avatar': avatar})


def signup_redirect(request):
    """
    The signup_redirect function redirects the user to the home page if they try to sign up with an email that is already in use.
    
    :param request: The request sent by the user
    :return: A redirect to the home page
    """
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect(to='chat_llm:home')


def user_plan_subscription(request):
    """
    The user_plan_subscription function is used to render the user_plan_subscription.html template,
    which displays a form that allows users to subscribe to a plan. The function takes in the request object as an argument,
    and returns the rendered user_plan_subscription.html template with context variables for 'users' and 'user_plan'.
    The 'users' variable contains all of the information about a particular User instance (i.e., username, email address), 
    while the 'user_plan' variable contains all of the information about a particular UserData instance (i.e., plan). 
    
    :param request: Get the user data from the database
    :return: The user_plan_subscription.html page with the user and user_plan
    """
    user = request.user
    user_plan = UserData.objects.get(user=user)
    return render(request, 'users/user_plan_subscription.html',
                  context={'users': user,
                           'user_plan': user_plan})


def user_statistic(request):
    """
    The user_statistic function is used to display the user's statistics.
        The function takes in a request object and returns a rendered template of the user_statistic.html page with context data.
    
    :param request: Get the user object from the request
    :return: A rendered template of the user_statistic.html page with context data
    """
    user = request.user
    user_data = UserData.objects.get(user=user)
    max_questions_allowed = user_data.max_questions_allowed_for_plan()
    max_files_allowed = user_data.max_files_allowed_for_plan()
    width_questions = user_data.total_questions_asked / max_questions_allowed * 100
    width_files = user_data.total_files_uploaded / max_files_allowed * 100
    return render(request, 'users/user_statistic.html',
                  context={'user': user,
                           'user_data': user_data,
                           "max_questions": max_questions_allowed,
                           "max_files": max_files_allowed,
                           "width_questions": width_questions,
                           "width_files": width_files,
                           })
