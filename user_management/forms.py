from django import forms
from user_management.models import Dealer_Profile

class DealerDeleteForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
            attrs={"placeholder": "Dealer Code", "class": "form-control"}))
    managed_by = forms.CharField(widget=forms.PasswordInput(
            attrs={"placeholder": "Manager's username", "class": "form-control"}))
    
class DealerForm(forms.ModelForm):
    code            = forms.CharField()
    auth_number     = forms.CharField()
    first_name      = forms.CharField()
    last_name       = forms.CharField()
    firm_name       = forms.CharField()
    pd_open_date    = forms.DateField()

    address     = forms.CharField()
    city        = forms.CharField()
    taluka      = forms.CharField()
    district    = forms.CharField()
    state       = forms.CharField()
    pin_code    = forms.CharField()
    contact     = forms.CharField()
    email       = forms.EmailField()

    pan_number          = forms.CharField()
    GST_number          = forms.CharField()
    seed_license        = forms.CharField()
    pesticide_license   = forms.CharField()
    fertilizer_license  = forms.CharField()
    SD_receipt_code     = forms.CharField()
    SD_expected         = forms.CharField()
    SD_deposited        = forms.CharField()
    SD_receipt_date     = forms.DateField()
    SD_payment_type     = forms.CharField()
    exp_first_order     = forms.CharField()

    managed_by      = forms.CharField()
    agreement_done  = forms.BooleanField()
    gift_sent       = forms.BooleanField()
    authorized      = forms.BooleanField()

    class Meta:
        model = Dealer_Profile
        fields = "__all__"
