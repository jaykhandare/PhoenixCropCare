from django.db import models


class Taxes(models.Model):
    name = models.CharField(max_length=7, blank=False, unique=True)
    rate = models.FloatField(blank=False)
