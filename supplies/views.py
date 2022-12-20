from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from vehicles.models import Vehicle

from .forms import SupplyForm
from .models import Supply


class SuccessURL(View):
    """Abstract class for add `get_success_url`. Do not use directly."""

    def get_success_url(self):
        return reverse_lazy(
            "supplies:list", kwargs={"slug": self.object.vehicle.slug}  # type:ignore
        )


class SupplyListView(LoginRequiredMixin, ListView):
    model = Supply
    template_name = "supplies/list.html"

    def get_queryset(self):
        return Supply.objects.filter(
            vehicle__slug=self.kwargs["slug"], vehicle__owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slug"] = self.kwargs["slug"]
        return context


class SupplyCreateView(LoginRequiredMixin, SuccessURL, CreateView):
    form_class = SupplyForm
    template_name = "supplies/edit.html"

    def get(self, *args, **kwargs):
        get_object_or_404(Vehicle, slug=self.kwargs["slug"], owner=self.request.user)
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        form.instance.vehicle = Vehicle.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)


class SupplyEditView(LoginRequiredMixin, SuccessURL, UpdateView):
    form_class = SupplyForm
    template_name = "supplies/edit.html"

    def get_queryset(self):
        return Supply.objects.filter(vehicle__owner=self.request.user)


class SupplyDeleteView(SuccessURL, DeleteView):
    model = Supply
