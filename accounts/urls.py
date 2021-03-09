from django.contrib.auth import views
from django.urls import path

from accounts.forms import (CustomPasswordResetForm, CustomSetPasswordForm,
                            LoginForm)

from .views import SignUpView, UserDetailView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("users/<username>", UserDetailView.as_view(), name="user-detail"),
     # Attach custom login form to default login view
    path(
        'login/',
        views.LoginView.as_view(
            authentication_form=LoginForm
            ),
        name='login'
    ),
    path(
        'password_reset/',
        views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm
            ),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm
            ),
        name='password_reset_confirm'
    ),
]
