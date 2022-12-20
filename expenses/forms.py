from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = (
            "title",
            "vendor",
            "category",
            "date",
            "mileage",
            "price",
            "attachment",
            "note",
        )
