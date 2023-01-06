from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    AppSettingsForm,
    PwdChangeForm,
    PwdResetConfirmForm,
    PwdResetForm,
    RegisterForm,
    SigninForm,
    UserForm,
)
from .models import AppSettings, User


class UserRegsiterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("vehicles:list")


class UserLoginView(LoginView):
    authentication_form = SigninForm
    template_name = "accounts/login.html"
    next_page = reverse_lazy("vehicles:list")


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


@login_required
def profile(request):
    """The code below creates a view for the profile page containing
    an account update form and an application settings form.
    """
    user_form = UserForm(request.POST or None, instance=request.user)

    try:
        instance_app_form = AppSettings.objects.get(user=request.user)
        app_form = AppSettingsForm(request.POST or None, instance=instance_app_form)
    except:
        app_form = AppSettingsForm(request.POST or None)

    if request.method == "POST":
        if user_form.is_valid():
            user_form.save()
        if app_form.is_valid():
            form = app_form.save(commit=False)
            form.user = request.user
            form.save()

        return redirect("accounts:profile")

    context = {"user_form": user_form, "app_form": app_form}

    return render(request, "accounts/profile.html", context)
