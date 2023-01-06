import json
import os

from django.core.management.base import BaseCommand

from accounts.models import Currency


class Command(BaseCommand):
    help = "Add currencies in database."

    CURRENT_DIR = os.path.dirname(__file__)

    def handle(self, *args, **kwargs):

        with open(os.path.join(self.CURRENT_DIR, "currencies.json"), "r") as file:
            data = json.load(file)

        for currency in data:
            Currency.objects.update_or_create(
                name=currency["name"],
                symbol=currency["symbol"],
                symbol_native=currency["symbolNative"],
                decimal_digits=currency["decimalDigits"],
                rounding=currency["rounding"],
                code=currency["code"],
                name_plural=currency["namePlural"],
            )
