from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import (
    UserLoginForm,
    UserPasswordChangeForm,
    UserPasswordResetConfirmForm,
    UserPasswordResetForm,
    UserProfileForm,
    UserRegisterForm,
)
from .models import User


class HomepageView(TemplateView):
    template_name = "accounts/homepage.html"


class UserRegsiterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:home")


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "accounts/login.html"
    next_page = reverse_lazy("accounts:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:home")


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:home")


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = UserPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:home")


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:login")


class UserPasswordResetDoneView(PasswordResetDoneView):
    form_class = UserPasswordResetConfirmForm
    template_name = "accounts/password_reset_done.html"
