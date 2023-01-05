from django.db import models
from django.utils.translation import gettext_lazy as _
from private_storage.fields import PrivateFileField

from vehicles.models import Vehicle

CATEGORIES = (
    ("maintenance", _("Maintenance")),
    ("repair", _("Repair")),
    ("administrative", _("Administrative")),
    ("various", _("Various")),
)


def upload_doc(instance, filename):
    return "documents/{slug}/{filename}".format(
        username=instance.vehicle.slug, filename=filename
    )


class ExpenseManager(models.Manager):
    def stats(self, vehicle):
        return Expense.objects.filter(vehicle=vehicle).aggregate(
            sum=models.Sum("price"),
            count=models.Count("title"),
            max=models.Max("mileage"),
        )


class Expense(models.Model):
    title = models.CharField(_("title"), max_length=128)
    vendor = models.CharField(_("vendor"), max_length=128, blank=True)
    category = models.CharField(
        _("category"), max_length=24, choices=CATEGORIES, default="maintenance"
    )
    date = models.DateField(_("date"))
    mileage = models.IntegerField(_("mileage"), blank=True, null=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, blank=True)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="expenses"
    )
    attachment = PrivateFileField(
        _("file"), upload_to=upload_doc, blank=True, null=True
    )
    note = models.TextField(blank=True)
    objects = ExpenseManager()

    class Meta:
        verbose_name = _("expense")
        ordering = ["-date"]

    def __str__(self):
        return self.title
