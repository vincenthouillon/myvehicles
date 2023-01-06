"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""
from django.conf import settings
from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/password/", UserPasswordChangeView.as_view(), name="password_change"),
    path("password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
]

if settings.SIGNUPS_ALLOWED:
    urlpatterns += [
        path("signup/", UserRegsiterView.as_view(), name="register"),
    ]
