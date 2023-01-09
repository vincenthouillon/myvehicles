from django.conf import settings
from django.contrib.auth import get_user_model
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
from django.views.generic import CreateView, UpdateView

from .forms import (
    PwdChangeForm,
    PwdResetConfirmForm,
    PwdResetForm,
    RegisterForm,
    SigninForm,
    UserForm,
)
from .models import User


class UserRegsiterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("vehicles:list")


class UserLoginView(LoginView):
    authentication_form = SigninForm
    template_name = "accounts/login.html"
    next_page = reverse_lazy("vehicles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signups_allowed"] = settings.SIGNUPS_ALLOWED
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PwdChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("vehicles:list")


class UserPasswordResetView(PasswordResetView):
    form_class = PwdResetForm
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = PwdResetConfirmForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:login")


class UserPasswordResetDoneView(PasswordResetDoneView):
    form_class = PwdResetConfirmForm
    template_name = "accounts/password_reset_done.html"


class Profile(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    model = get_user_model()
    form_class = UserForm

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"pk": self.kwargs["pk"]})
