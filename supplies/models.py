from django.db import models
from django.utils.translation import gettext_lazy as _
from private_storage.fields import PrivateFileField

from vehicles.models import FUELTYPE, Vehicle


def upload_doc(instance, filename):
    return "documents/{slug}/{filename}".format(
        slug=instance.vehicle.slug, filename=filename
    )


class Supply(models.Model):
    vendor = models.CharField(_("vendor"), max_length=128, blank=True)
    fueltype = models.CharField(
        _("Fuel type"), max_length=24, choices=FUELTYPE, default="diesel"
    )
    date = models.DateField(_("date"))
    mileage = models.IntegerField(_("mileage"), blank=True, null=True)
    number_of_liters = models.DecimalField(
        _("number of liters"), max_digits=6, decimal_places=2, blank=True, null=True
    )
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    full_tank = models.BooleanField(_("full tank"), default=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="fuels")
    attachment = PrivateFileField(
        _("file"), upload_to=upload_doc, blank=True, null=True
    )
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _("fuel")
        ordering = ["-date"]

    @property
    def price_per_liters(self):
        return round(self.price / self.number_of_liters, ndigits=2)  # type:ignore

    def __str__(self):
        return f"{self.date}-{self.vendor}"
