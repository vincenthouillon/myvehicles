from django import forms

from .models import Supply


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = (
            "vendor",
            "fueltype",
            "date",
            "mileage",
            "number_of_liters",
            "price",
            "full_tank",
            "attachment",
            "note",
        )
