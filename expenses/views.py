from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from vehicles.models import Vehicle

from .forms import ExpenseForm
from .models import Expense


class Mixin(View):
    """Abstract class for add `get_success_url` and `get_context_data` with
    vehicle instance. Do not use directly.
    """

    def get_success_url(self):
        return reverse_lazy(
            "expenses:list", kwargs={"slug": self.object.vehicle.slug}  # type:ignore
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


class ExpenseListView(LoginRequiredMixin, Mixin, ListView):
    model = Expense
    template_name = "expenses/list.html"
    paginate_by = 20

    def get_queryset(self):
        return Expense.objects.filter(
            vehicle__slug=self.kwargs["slug"], vehicle__owner=self.request.user
        )


class ExpenseCreateView(LoginRequiredMixin, Mixin, CreateView):
    form_class = ExpenseForm
    template_name = "expenses/edit.html"

    def get(self, *args, **kwargs):
        get_object_or_404(Vehicle, slug=self.kwargs["slug"], owner=self.request.user)
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        form.instance.vehicle = Vehicle.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)


class ExpenseEditView(LoginRequiredMixin, Mixin, UpdateView):
    form_class = ExpenseForm
    template_name = "expenses/edit.html"

    def get_queryset(self):
        return Expense.objects.filter(vehicle__owner=self.request.user)


class ExpenseDeleteView(LoginRequiredMixin, Mixin, DeleteView):
    model = Expense
