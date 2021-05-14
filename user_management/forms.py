from django import forms

class DealerDeleteForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
            attrs={"placeholder": "Dealer Code", "class": "form-control"}))
    managed_by = forms.CharField(widget=forms.TextInput(
            attrs={"placeholder": "Manager's username", "class": "form-control"}))


class UserDeleteForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}))
    email = forms.CharField(widget=forms.TextInput(
            attrs={"placeholder": "email", "class": "form-control"}))
