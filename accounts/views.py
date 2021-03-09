from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import User

from .forms import LoginForm, SignUpForm

from django.contrib.messages.views import SuccessMessageMixin

class SignUpView(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_message = "Success! Welcome to Cookery Bookery."

    def get_success_url(self):
        username = self.request.POST['username']
        return reverse_lazy("user-detail", args=[username])

    def form_valid(self, form):
        super().form_valid(form)
        # Save the new user
        form.save()
        # Get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # Authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "registration/user_detail.html"

    def get_object(self):
        return User.objects.get(username=self.request.user)
