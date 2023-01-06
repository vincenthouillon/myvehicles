import calendar
from datetime import datetime
from decimal import Decimal
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.utils import timezone
from django.views.generic import ListView, TemplateView

from accounts.models import AppSettings
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


class MonthlyGraph:
    """Returns a dictionary with the months of the year and the sum
    of the expenses and supplies for each month.
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle

    def __populate(self, model):
        YEAR = timezone.now().year
        data_list = list()
        for d in range(1, 13):
            aggr = (
                model.objects.filter(vehicle=self.vehicle)
                .filter(
                    date__range=(
                        datetime(YEAR, d, 1),
                        datetime(YEAR, d, calendar.monthrange(YEAR, d)[1]),
                    )
                )
                .aggregate(sum=Sum("price"))
            )
            aggr["sum"] = float(aggr["sum"]) if aggr["sum"] else 0.0
            data_list.append(aggr["sum"])
        return data_list

    def __call__(self):
        return {
            "month_list": list(calendar.month_name)[1:],
            "supplies_data": self.__populate(Supply),
            "expenses_data": self.__populate(Expense),
        }


class ExpenseByCategory:
    """returns a dictionary with the labels and data for the
    expense by category chart.
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle

    def __call__(self):
        category_labels = list()
        category_data = list()
        qs_category = (
            Expense.objects.filter(vehicle=self.vehicle)
            .values("category")
            .annotate(sum=Sum("price"), count=Count("title"))
        )
        for query in qs_category:
            name = qs_category.model(
                category=query["category"]
            ).get_category_display()  # type:ignore
            query["category"] = name
            category_labels.append(name)
            category_data.append(float(query["sum"]))

        return {
            "category_labels": category_labels,
            "category_data": category_data,
            "query_expense": qs_category,
        }


class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "stats/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Dataset(self.kwargs["slug"])
        context["vehicle"] = data.vehicle
        context["data"] = data
        context["monthly_graph_data"] = MonthlyGraph(data.vehicle)
        context["expenses_category"] = ExpenseByCategory(data.vehicle)
        context["last_mileage"] = _last_mileage(data.vehicle)
        context["settings"] = AppSettings.objects.get(user=self.request.user)
        return context


class AllCostsView(LoginRequiredMixin, ListView):
    template_name = "stats/allcosts.html"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.vehicle = Vehicle.objects.get(slug=self.kwargs["slug"])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        expenses = Expense.objects.filter(vehicle=self.vehicle)
        supplies = Supply.objects.filter(vehicle=self.vehicle)
        all_costs = sorted(
            chain(expenses, supplies), key=lambda instance: instance.date, reverse=True
        )
        return all_costs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehicle"] = self.vehicle
        context["settings"] = AppSettings.objects.get(user=self.request.user)
        return context
