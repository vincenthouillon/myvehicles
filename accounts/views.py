from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from .forms import (
    UserLoginForm,
    UserPasswordChangeForm,
    UserProfileForm,
    UserRegisterForm,
)
from .models import User


class HomepageView(TemplateView):
    template_name = "registration/homepage.html"


class UserRegsiterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("accounts:home")


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "registration/login.html"
    next_page = reverse_lazy("accounts:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:home")


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("accounts:home")


class UserPasswordChangeView(PasswordChangeView):
    model = User
    form_class = UserPasswordChangeForm
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("accounts:home")
