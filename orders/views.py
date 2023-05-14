from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from cart.models import CartItem

# Create your views here.
@login_required
def orders_view(request):
    orders = Order.valid_orders.filter(user_id=request.user.id)
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'orders/order_details.html', context)


def order_placed(request):
    items = CartItem.objects.filter(user_id=request.user.id)
    items.delete()
    return render(request, 'orders/order_placed.html')

