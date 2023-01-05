import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Supply


class SupplyForm(forms.ModelForm):
    date = forms.DateField(
        label=_("Date"),
        initial=datetime.date.today,
        widget=forms.TextInput(attrs={"type": "date"}),
    )

    attachment = forms.FileField(label=_("File"), required=False)
    full_tank = forms.BooleanField(
        label=_("full tank"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )
    note = forms.CharField(
        label=_("Note"), required=False, widget=forms.Textarea(attrs={"rows": 6})
    )

    class Meta:
        model = Supply
        exclude = ("vehicle",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control form-control-sm"
