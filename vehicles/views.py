from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from expenses.models import Expense
from supplies.models import Supply

from .forms import VehicleForm
from .models import Vehicle


class Mixin(View):
    """Abstract class for filter users and add `success_url`. Do not use directly."""

    def get_queryset(self):
        """Filter vehicles by user."""
        return Vehicle.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("vehicles:list")


class VehicleHomeView(LoginRequiredMixin, Mixin, TemplateView):
    template_name = "vehicles/home.html"

    def get_context_data(self, **kwargs):
        vehicle = Vehicle.objects.get(slug=self.kwargs["slug"])
        context = super().get_context_data(**kwargs)
        context["vehicle"] = vehicle
        context["supplies"] = Supply.objects.filter(vehicle=vehicle)[:10]
        context["expenses"] = Expense.objects.filter(vehicle=vehicle)[:10]
        return context


class VehicleListView(LoginRequiredMixin, Mixin, ListView):
    model = Vehicle
    template_name = "vehicles/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.username == "changeme":  # type:ignore
            messages.add_message(
                self.request,
                messages.ERROR,
                _(
                    "You need to change the username and password of the `changeme` account."
                ),
                extra_tags="alert alert-danger",
            )
        return context


class VehicleCreateView(LoginRequiredMixin, Mixin, CreateView):
    form_class = VehicleForm
    template_name = "vehicles/edit.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.is_active = True
        self.object.save()
        return super().form_valid(form)


class VehicleEditView(LoginRequiredMixin, Mixin, UpdateView):
    form_class = VehicleForm
    template_name = "vehicles/edit.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.POST.get("id_is_active"):
            try:
                self.object.is_active = True
                self.object.save()
            except IntegrityError:
                messages.warning(
                    self.request,
                    _("You already have a vehicle with this name."),
                    extra_tags="alert alert-warning",
                )
        return super().form_valid(form)


class VehicleDeleteView(Mixin, DeleteView):
    model = Vehicle
