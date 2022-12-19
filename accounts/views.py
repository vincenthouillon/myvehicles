from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import UserLoginForm, UserRegisterForm
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
