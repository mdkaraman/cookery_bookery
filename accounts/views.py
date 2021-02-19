from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserDetailView(LoginRequiredMixin, generic.DetailView):  
    model = User
    template_name = 'registration/user_detail.html'

    def get_object(self):
        return User.objects.get(username=self.request.user)
    