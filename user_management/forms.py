from django import forms
from user_management.models import Dealer_Profile

class DealerDeleteForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
            attrs={"placeholder": "Dealer Code", "class": "form-control"}))
    managed_by = forms.CharField(widget=forms.PasswordInput(
            attrs={"placeholder": "Manager's username", "class": "form-control"}))

