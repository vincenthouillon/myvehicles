from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from private_storage.fields import PrivateImageField

User = get_user_model()

FUELTYPE = [
    ("diesel", _("diesel")),
    ("petrol", _("petrol")),
    ("ethanol", _("ethanol")),
    ("electric", _("electric")),
    ("cng", _("CNG")),  # Compressed Natural Gas
    ("lpg", _("LPG")),  # Liquified Petroleum Gas
]

FUELUNIT = [
    ("L", _("liter")),
    ("gal", _("gallon")),
    ("kg", _("kilogram")),
    ("KWh", _("kilowatt hour")),
    ("min", _("minutes")),
]


def upload_img(instance, filename):
    return "pictures/{slug}/{filename}".format(slug=instance.slug, filename=filename)


class Vehicle(models.Model):
    name = models.CharField(_("name"), max_length=32, unique=True)
    description = models.CharField(_("description"), max_length=128, blank=True)
    manufacturer = models.CharField(_("manufacturer"), max_length=64, blank=True)
    model = models.CharField(_("model"), max_length=64, blank=True)
    horsepower = models.IntegerField(_("horsepower"), default=0)
    fuel_type = models.CharField(
        _("fuel type"), choices=FUELTYPE, max_length=32, default="diesel"
    )
    fuel_unit = models.CharField(
        _("fuel unit"), choices=FUELUNIT, max_length=32, default="L"
    )
    mileage = models.IntegerField(_("mileage"), blank=True, null=True)
    tank_size = models.IntegerField(_("tank size"), default=0)
    date_first_registration = models.DateField(
        _("date of 1st circulation"), blank=True, null=True
    )
    registration = models.CharField(
        _("registration"), max_length=20, blank=True, null=True
    )
    price = models.DecimalField(
        _("price"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    date_purchase = models.DateField(_("date purchase"), blank=True, null=True)
    note = models.TextField(_("note"), blank=True)
    picture = PrivateImageField(
        _("picture"), upload_to=upload_img, blank=True, null=True
    )
    is_active = models.BooleanField(_("is active"), default=True)
    inactive_since = models.DateField(_("inactive since"), blank=True, null=True)
    # ---
    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("vehicle")
        ordering = ["-is_active", "name"]
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="owner_vehicle")
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
