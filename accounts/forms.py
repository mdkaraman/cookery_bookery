from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class SignUpForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['email'].widget.attrs.update({'class': 'input', 'type': 'email'})
        self.fields['password1'].widget.attrs.update({'class': 'input', 'type': 'password'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'type': 'password'})

    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=200)

    def clean(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _(
                    "This email address belongs to an existing account! Enter a new email."
                )
            )
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input', 'type': 'password'})
  