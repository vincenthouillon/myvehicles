from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from accounts.models import AppSettings
from stats.views import _last_mileage
from vehicles.models import Vehicle

from .forms import SupplyForm
from .models import Supply


class Mixin(View):
    """Abstract class for add `get_success_url` and `get_context_data` with
    vehicle instance. Do not use directly.
    """

    def get_success_url(self):
        return reverse_lazy(
            "supplies:list", kwargs={"slug": self.object.vehicle.slug}  # type:ignore
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # type:ignore
        try:
            context["vehicle"] = Vehicle.objects.get(
                slug=self.kwargs["slug"]  # type:ignore
            )
        except KeyError:
            context["vehicle"] = Vehicle.objects.get(
                slug=self.object.vehicle.slug  # type:ignore
            )
        return context


class SupplyListView(LoginRequiredMixin, Mixin, ListView):
    model = Supply
    template_name = "supplies/list.html"
    paginate_by = 20

    def get_queryset(self):
        return Supply.objects.filter(
            vehicle__slug=self.kwargs["slug"], vehicle__owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = AppSettings.objects.get(user=self.request.user)
        return context


class SupplyCreateView(LoginRequiredMixin, Mixin, CreateView):
    form_class = SupplyForm
    template_name = "supplies/edit.html"

    def form_valid(self, form):
        form.instance.vehicle = Vehicle.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        vehicle = Vehicle.objects.get(slug=self.kwargs["slug"], owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context["last_mileage"] = _last_mileage(vehicle)
        return context


class SupplyEditView(LoginRequiredMixin, Mixin, UpdateView):
    form_class = SupplyForm
    template_name = "supplies/edit.html"

    def get_queryset(self):
        return Supply.objects.filter(vehicle__owner=self.request.user)


class SupplyDeleteView(LoginRequiredMixin, Mixin, DeleteView):
    model = Supply
