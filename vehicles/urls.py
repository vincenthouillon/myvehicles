"""vehicle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    VehicleCreateView,
    VehicleDeleteView,
    VehicleEditView,
    VehicleHomeView,
    VehicleListView,
)

app_name = "vehicles"

urlpatterns = [
    path("", VehicleListView.as_view(), name="list"),
    path("add/", VehicleCreateView.as_view(), name="add"),
    path("<slug:slug>/home/", VehicleHomeView.as_view(), name="home"),
    path("<slug:slug>/edit/", VehicleEditView.as_view(), name="edit"),
    path("<slug:slug>/delete/", VehicleDeleteView.as_view(), name="delete"),
]
