from django.db import models

from menu.models import Menu, Serving
from accounts.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=50, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    serving = models.ForeignKey(Serving, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


