from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from .forms import VehicleForm
from .models import Vehicle


class UserFilter(View):
    """Abstract class for filter users. Do not use directly."""

    def get_queryset(self):
        """Filter vehicles by user."""
        return Vehicle.objects.filter(owner=self.request.user)


class VehicleListView(LoginRequiredMixin, UserFilter, ListView):
    model = Vehicle
    template_name = "vehicles/list.html"


class VehicleCreateView(LoginRequiredMixin, CreateView):
    form_class = VehicleForm
    template_name = "vehicles/edit.html"
    success_url = reverse_lazy("vehicles:list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class VehicleEditView(LoginRequiredMixin, UserFilter, UpdateView):
    form_class = VehicleForm
    template_name = "vehicles/edit.html"
    success_url = reverse_lazy("vehicles:list")


class VehicleDeleteView(UserFilter, DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicles:list")
