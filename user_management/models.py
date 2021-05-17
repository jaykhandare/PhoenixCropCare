from django.db import models


class User_Profile(models.Model):
    username    = models.CharField(max_length=20, unique=True)

    address     = models.CharField(max_length=30, blank=True)
    city        = models.CharField(max_length=15, blank=True)
    taluka      = models.CharField(max_length=15, blank=True)
    district    = models.CharField(max_length=15, blank=True)
    state       = models.CharField(max_length=15, blank=True)
    pin_code    = models.CharField(max_length=6, blank=True)

    date_of_birth   = models.DateField(null=True, blank=True)
    contact         = models.CharField(max_length=12, blank=True)

    e_verified      = models.BooleanField(default=False)
    position        = models.CharField(max_length=15, blank=True)
    manager         = models.CharField(max_length=20)
    authorized      = models.BooleanField(default=False)
    date_of_joining = models.DateField(null=True, blank=True)


class Dealer_Profile(models.Model):
    firm_name       = models.CharField(max_length=35, unique=True)
    code            = models.CharField(max_length=20, blank=True)
    auth_number     = models.CharField(max_length=20, blank=True)
    first_name      = models.CharField(max_length=20, blank=True)
    last_name       = models.CharField(max_length=20, blank=True)
    pd_open_date    = models.DateField(null=True, blank=True)

    address     = models.CharField(max_length=30, blank=True)
    city        = models.CharField(max_length=15, blank=True)
    taluka      = models.CharField(max_length=15, blank=True)
    district    = models.CharField(max_length=15, blank=True)
    state       = models.CharField(max_length=15, blank=True)
    pin_code    = models.CharField(max_length=6, blank=True)
    contact     = models.CharField(max_length=15, unique=True)
    email       = models.EmailField(blank=True)

    pan_number          = models.CharField(max_length=15, blank=True)
    GST_number          = models.CharField(max_length=20, blank=True)
    seed_license        = models.CharField(max_length=20, blank=True)
    pesticide_license   = models.CharField(max_length=20, blank=True)
    fertilizer_license  = models.CharField(max_length=20, blank=True)
    SD_receipt_code     = models.CharField(max_length=20, blank=True)
    SD_expected         = models.CharField(max_length=15, blank=True)
    SD_deposited        = models.CharField(max_length=15, blank=True)
    SD_receipt_date     = models.DateField(null=True, blank=True)
    SD_payment_type     = models.CharField(max_length=30, blank=True)
    exp_first_order     = models.CharField(max_length=30, blank=True)

    managed_by      = models.CharField(max_length=20, blank=False)
    agreement_done  = models.BooleanField(default=False)
    gift_sent       = models.BooleanField(default=False)
    authorized      = models.BooleanField(default=False)
