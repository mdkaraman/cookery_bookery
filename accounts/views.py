from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import User

from .forms import LoginForm, SignUpForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Save the new user
        form.save()
        # Get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # Authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy("user-detail", args=[username]))

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "registration/user_detail.html"

    def get_object(self):
        return User.objects.get(username=self.request.user)
