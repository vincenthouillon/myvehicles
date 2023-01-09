from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    """For populate with currencies.json.
    Command : python manage.py addcurrencies
    """

    name = models.CharField(_("name"), max_length=40)
    symbol = models.CharField(_("symbol"), max_length=5)
    symbol_native = models.CharField(_("symbol native"), max_length=6)
    decimal_digits = models.IntegerField(_("decimal digit"))
    rounding = models.IntegerField(_("rounding"))
    code = models.CharField(_("code"), max_length=5)
    name_plural = models.CharField(_("name plural"), max_length=40)

    class Meta:
        verbose_name = "devise"
        ordering = ["code"]

    def __str__(self):
        return self.code


class User(AbstractUser):
    """AbstractUser with additional fields `currency` and `distance_unit`."""

    DISTANCE_CHOICES = (
        ("Km", _("kilometers")),
        ("Mi", _("miles")),
    )
    currency = models.ForeignKey(
        Currency, verbose_name=_("currency"), on_delete=models.CASCADE, null=True
    )
    distance_unit = models.CharField(
        _("distance unit"), max_length=24, choices=DISTANCE_CHOICES, default="Km"
    )

    class Meta:
        verbose_name = _("user")

    def __str__(self):
        return self.username
