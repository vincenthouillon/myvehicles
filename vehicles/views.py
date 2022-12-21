from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from .forms import VehicleForm
from .models import Vehicle


class Mixin(View):
    """Abstract class for filter users and add `success_url`. Do not use directly."""

    def get_queryset(self):
        """Filter vehicles by user."""
        return Vehicle.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("vehicles:list")


class VehicleListView(LoginRequiredMixin, Mixin, ListView):
    model = Vehicle
    template_name = "vehicles/list.html"


class VehicleCreateView(LoginRequiredMixin, Mixin, CreateView):
    form_class = VehicleForm
    template_name = "vehicles/edit.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class VehicleEditView(LoginRequiredMixin, Mixin, UpdateView):
    form_class = VehicleForm
    template_name = "vehicles/edit.html"


class VehicleDeleteView(Mixin, DeleteView):
    model = Vehicle
