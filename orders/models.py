from django.db import models
from django.db.models.query import QuerySet

from accounts.models import User, ShippingAddress
from menu.models import Menu, Serving


class PaidOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(payment_status=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping = models.OneToOneField(ShippingAddress, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_amount = models.CharField(max_length=100)
    order_key = models.CharField(max_length=200)
    payment_status = models.BooleanField(default=False)
    objects = models.Manager()
    valid_orders = PaidOrderManager()

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return str(self.created)
    
    def order_status(self):
        if self.payment_status:
            return 'Paid'
        else:
            return 'Not paid'
        
    def total(self):
        return float(self.total_amount) / 100
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    serving = models.ForeignKey(Serving, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    
    def sub_total(self):
        return self.quantity * self.sub_price