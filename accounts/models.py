from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # add any additional fields or methods here
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    postcode = models.CharField(max_length=10)
    address1 = models.CharField(max_length=80)
    address2 = models.CharField(max_length=80, blank=True, null=True)
    town = models.CharField(max_length=80)
    contact_number = models.CharField(max_length=20)
    remarks = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}  {self.address1} {self.address2}, {self.town}   {self.contact_number}"
