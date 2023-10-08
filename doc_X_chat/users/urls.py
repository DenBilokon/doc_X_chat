from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, FormView
from .forms import LoginForm
from .views import RegisterView, ResetPasswordView, profile, upload_avatar, signup_redirect, update_user, \
    user_plan_subscription, activate_account

app_name = "users"

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('signin/', LoginView.as_view(
        template_name='users/signin.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('user_upload_avatar/', upload_avatar, name='upload_avatar'),
    path('profile/', profile, name='profile'),
    path('social/signup/', signup_redirect, name='signup_redirect'),
    path('update_user/', update_user, name='update_user'),
    path('user_plan_subscription/', user_plan_subscription, name='user_plan_subscription'),
    path('activate/<str:uid>/<str:token>/', activate_account, name='activate')

]
