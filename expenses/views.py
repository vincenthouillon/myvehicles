from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from vehicles.models import Vehicle

from .forms import ExpenseForm
from .models import Expense


class SuccessURL(View):
    """Abstract class for add `get_success_url`. Do not use directly."""

    def get_success_url(self):
        return reverse_lazy(
            "expenses:list", kwargs={"slug": self.object.vehicle.slug}  # type:ignore
        )


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "expenses/list.html"

    def get_queryset(self):
        return Expense.objects.filter(
            vehicle__slug=self.kwargs["slug"], vehicle__owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slug"] = self.kwargs["slug"]
        return context


class ExpenseCreateView(LoginRequiredMixin, SuccessURL, CreateView):
    form_class = ExpenseForm
    template_name = "expenses/edit.html"

    def get(self, *args, **kwargs):
        get_object_or_404(Vehicle, slug=self.kwargs["slug"], owner=self.request.user)
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        form.instance.vehicle = Vehicle.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)


class ExpenseEditView(LoginRequiredMixin, SuccessURL, UpdateView):
    form_class = ExpenseForm
    template_name = "expenses/edit.html"

    def get_queryset(self):
        return Expense.objects.filter(vehicle__owner=self.request.user)


class ExpenseDeleteView(SuccessURL, DeleteView):
    model = Expense
