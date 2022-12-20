from django import forms

from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "name",
            "description",
            "manufacturer",
            "model",
            "horsepower",
            "fuel_type",
            "fuel_unit",
            "mileage",
            "tank_size",
            "date_first_registration",
            "registration",
            "price",
            "date_purchase",
            "note",
            "picture",
        )
