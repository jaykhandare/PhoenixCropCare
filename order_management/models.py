from django.db import models


class Product(models.Model):
    type    = models.CharField(max_length=20, blank=False)
    name    = models.CharField(max_length=25, blank=False)
    price   = models.FloatField(blank=False)
    details = models.TextField(blank=True)
    uom     = models.CharField(max_length=7, blank=True)


class Order(models.Model):
    invoice_number  = models.PositiveIntegerField(blank=False)
    product_code    = models.PositiveIntegerField(blank=False)
    quantity        = models.PositiveIntegerField(blank=False)
    total_price     = models.FloatField(blank=False)

class Transaction(models.Model):
    invoice_number      = models.PositiveIntegerField(unique=True)
    customer_code       = models.CharField(max_length=20, blank=False)
    mode_of_transport   = models.CharField(max_length=15, blank=True)
    total_pre_tax       = models.FloatField(default=0)
    discount_percent    = models.FloatField(default=0)
    total_price_taxed   = models.FloatField(default=0)
    payment_type        = models.CharField(max_length=30, blank=True)
    is_accepted         = models.BooleanField(default=False)
    is_dispatched       = models.BooleanField(default=False)
    is_closed           = models.BooleanField(default=False)
    dateTime            = models.DateTimeField(auto_now_add=True)
