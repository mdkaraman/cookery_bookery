from django.contrib.auth import views
from django.urls import path

from accounts.forms import LoginForm

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
]
