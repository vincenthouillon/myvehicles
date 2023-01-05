import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CATEGORIES, Expense


class ExpenseForm(forms.ModelForm):
    category = forms.CharField(
        label=_("Category"), widget=forms.Select(choices=CATEGORIES)
    )
    date = forms.DateField(
        label=_("Date"),
        initial=datetime.date.today,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    title = forms.CharField(label=_("Title"))
    vendor = forms.CharField(label=_("Vendor"), required=False)
    price = forms.DecimalField(
        label=_("Total"),
        initial=0.0,
        decimal_places=2,
        widget=forms.TextInput(attrs={"type": "number", "step": "any"}),
    )
    mileage = forms.IntegerField(
        label=_("Mileage"),
        required=False,
        widget=forms.TextInput(attrs={"type": "number"}),
    )
    note = forms.CharField(
        label=_("Note"), required=False, widget=forms.Textarea(attrs={"rows": 6})
    )
    attachment = forms.FileField(label=_("File"), required=False)

    class Meta:
        model = Expense
        fields = "__all__"
        exclude = ("vehicle",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control form-control-sm"
