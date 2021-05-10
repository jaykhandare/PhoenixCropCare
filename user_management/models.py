from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=20, unique=True)

    address = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    taluka = models.CharField(max_length=15)
    district = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=6)

    date_of_birth = models.DateField(auto_now_add=True)
    contact = models.CharField(max_length=12)

    e_verified = models.BooleanField(default=False)
    position = models.CharField(max_length=15)
    manager = models.CharField(max_length=20)
    authorized = models.BooleanField(default=False)
    date_of_joining = models.DateField(auto_now_add=True)
