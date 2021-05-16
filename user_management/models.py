from django.db import models


class User_Profile(models.Model):
    username    = models.CharField(max_length=20, unique=True)

    address     = models.CharField(max_length=30)
    city        = models.CharField(max_length=15)
    taluka      = models.CharField(max_length=15)
    district    = models.CharField(max_length=15)
    state       = models.CharField(max_length=15)
    pin_code    = models.CharField(max_length=6)

    date_of_birth   = models.DateField(auto_now_add=True)
    contact         = models.CharField(max_length=12)

    e_verified      = models.BooleanField(default=False)
    position        = models.CharField(max_length=15)
    manager         = models.CharField(max_length=20)
    authorized      = models.BooleanField(default=False)
    date_of_joining = models.DateField(auto_now_add=True)


class Dealer_Profile(models.Model):
    code            = models.CharField(max_length=20)
    auth_number     = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=20)
    last_name       = models.CharField(max_length=20)
    firm_name       = models.CharField(max_length=35, unique=True)
    pd_open_date    = models.DateField(auto_now_add=True)

    address     = models.CharField(max_length=30)
    city        = models.CharField(max_length=15)
    taluka      = models.CharField(max_length=15)
    district    = models.CharField(max_length=15)
    state       = models.CharField(max_length=15)
    pin_code    = models.CharField(max_length=6)
    contact     = models.CharField(max_length=30)
    email       = models.EmailField()

    pan_number          = models.CharField(max_length=15)
    GST_number          = models.CharField(max_length=20)
    seed_license        = models.CharField(max_length=20)
    pesticide_license   = models.CharField(max_length=20)
    fertilizer_license  = models.CharField(max_length=20)
    SD_receipt_code     = models.CharField(max_length=20)
    SD_expected         = models.CharField(max_length=15)
    SD_deposited        = models.CharField(max_length=15)
    SD_receipt_date     = models.DateField(auto_now_add=True)
    SD_payment_type     = models.CharField(max_length=30)
    exp_first_order     = models.CharField(max_length=30)

    managed_by      = models.CharField(max_length=20, blank=False)
    agreement_done  = models.BooleanField(default=False)
    gift_sent       = models.BooleanField(default=False)
    authorized      = models.BooleanField(default=False)
