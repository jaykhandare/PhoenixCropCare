from django.db import models


class Product(models.Model):
    type    = models.CharField(max_length=20, blank=False)
    name    = models.CharField(max_length=25, blank=False)
    price   = models.FloatField(blank=False)


class Order(models.Model):
    trans_code      = models.CharField(max_length=15, blank=False)
    product_code    = models.CharField(max_length=7, blank=False)
    quntity         = models.CharField(max_length=3, blank=False)
    uom             = models.CharField(max_length=7, blank=False)
    total_price     = models.FloatField(blank=False)

class Transaction(models.Model):
    trans_code          = models.CharField(max_length=15, unique=True)
    customer_code       = models.CharField(max_length=20, blank=False)
    mode_of_transport   = models.CharField(max_length=15, blank=True)
    invoice_number      = models.CharField(max_length=7, blank=False)
    total_pre_tax       = models.FloatField(blank=False)
    discount            = models.FloatField(default=0)
    total_price_taxed   = models.FloatField(blank=False)
    is_dispatched       = models.BooleanField(default=False)
    is_closed           = models.BooleanField(default=False)
