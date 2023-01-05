from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Vehicle


class VehicleForm(forms.ModelForm):

    picture = forms.ImageField(
        label=_("Picture"), required=False, widget=forms.FileInput
    )

    purchase_date = forms.DateField(
        label=_("Purchase date"),
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    note = forms.CharField(
        label=_("Note"), required=False, widget=forms.Textarea(attrs={"rows": 6})
    )
    date_released = forms.DateField(
        label=_("Date of 1st circulation"),
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    is_active = forms.BooleanField(
        label=_("Active"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )
    inactive_since = forms.DateField(
        label=_("Inactive since"),
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Vehicle
        exclude = ("owner", "slug")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control form-control-sm"
