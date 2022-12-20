"""supplies URL Configuration

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

from .views import SupplyCreateView, SupplyDeleteView, SupplyEditView, SupplyListView

app_name = "supplies"

urlpatterns = [
    path("<slug:slug>/all/", SupplyListView.as_view(), name="list"),
    path("<slug:slug>/add/", SupplyCreateView.as_view(), name="add"),
    path("edit/<int:pk>/", SupplyEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", SupplyDeleteView.as_view(), name="delete"),
]
