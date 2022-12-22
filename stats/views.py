from decimal import Decimal
from itertools import chain

from django.views.generic import TemplateView

from expenses.models import Expense
from supplies.models import Supply
from vehicles.models import Vehicle


def _last_mileage(vehicle):
    """Returns the last mileage record, based on the last 2 supplies
    and expenses.
    """
    supplies_filter = Supply.objects.filter(vehicle=vehicle)[:2]
    expenses_filter = Expense.objects.filter(vehicle=vehicle)[:2]
    last_mileage = sorted(
        chain(expenses_filter, supplies_filter),
        key=lambda instance: instance.date,
        reverse=True,
    )
    return last_mileage[0].mileage if last_mileage else 0


class Dataset:
    def __init__(self, vehicle_slug):
        slug = vehicle_slug
        self.vehicle = Vehicle.objects.get(slug=slug)
        self.supply_stat = Supply.objects.stats(self.vehicle)
        self.expense_stat = Expense.objects.stats(self.vehicle)
        self.supply_percent = self.__percent(self.supply_stat["sum"], self.all_costs)
        self.expense_percent = self.__percent(self.expense_stat["sum"], self.all_costs)
        self.last_mileage = _last_mileage(self.vehicle)
        self.kilometers = self.last_mileage - self.vehicle.mileage

    @property
    def all_costs(self):
        expense = self.expense_stat["sum"] if self.expense_stat["sum"] else Decimal("0")
        supply = self.supply_stat["sum"] if self.supply_stat["sum"] else Decimal("0")
        return expense + supply

    def __percent(self, obj, all_costs):
        return (obj / all_costs * 100) if all_costs and obj else Decimal("0")


class StatsView(TemplateView):
    template_name = "stats/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Dataset(self.kwargs["slug"])
        context["vehicle"] = data.vehicle
        context["data"] = data
        return context
