from django import forms
from .models import Window, Donor


def is_donor_id(value):
    if not Donor.objects.filter(pk=value):
        raise forms.ValidationError('Donor ID not found')


class DonorIdForm(forms.Form):
    donor_id = forms.CharField(validators=[is_donor_id])


class SelectForm(forms.Form):
    window = forms.ModelChoiceField(queryset=Window.objects.filter(sponsor=None))
    plaque = forms.CharField(max_length=200)


class SubmitForm(forms.Form):
    pass