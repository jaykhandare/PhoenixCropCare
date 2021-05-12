from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name="format_label")
@stringfilter
def format_label(value):
    # capitalize_labels = ["code", "address", "city", "taluka", "district", "state", "contact", "email", "authorized", "position"]

    if  "_" not in value:
        return value.capitalize()

    if value == "exp_first_order":
        return "Expected 1st order"

    if "SD" in value:
        value = value.replace("SD", "Secure-deposit")

    if "_" in value:
        value = " ".join([x.capitalize() for x in value.split("_")])
        return value

# print(format_label("SD_receipt_code"))

    # code            = models.CharField(max_length=20)
    # auth_number     = models.CharField(max_length=20)
    # first_name      = models.CharField(max_length=20)
    # last_name       = models.CharField(max_length=20)
    # firm_name       = models.CharField(max_length=35)
    # pd_open_date    = models.DateField(auto_now_add=True)

    # address     = models.CharField(max_length=30)
    # city        = models.CharField(max_length=15)
    # taluka      = models.CharField(max_length=15)
    # district    = models.CharField(max_length=15)
    # state       = models.CharField(max_length=15)
    # pin_code    = models.CharField(max_length=6)
    # contact     = models.CharField(max_length=30)
    # email       = models.EmailField()

    # pan_number          = models.CharField(max_length=15)
    # GST_number          = models.CharField(max_length=20)
    # seed_license        = models.CharField(max_length=20)
    # pesticide_license   = models.CharField(max_length=20)
    # fertilizer_license  = models.CharField(max_length=20)
    # SD_receipt_code     = models.CharField(max_length=20)
    # SD_expected         = models.CharField(max_length=15)
    # SD_deposited        = models.CharField(max_length=15)
    # SD_receipt_date     = models.DateField(auto_now_add=True)
    # SD_payment_type     = models.CharField(max_length=30)
    # exp_first_order     = models.CharField(max_length=30)

    # managed_by      = models.CharField(max_length=20)
    # agreement_done  = models.BooleanField(default=False)
    # gift_sent       = models.BooleanField(default=False)
    # authorized      = models.BooleanField(default=False)

