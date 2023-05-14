from django.db.models import F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import Cart, CartItem
from .cart import Cart


def cart_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        items = CartItem.objects.filter(user_id=user_id)
    else:
        items = CartItem.objects.filter(session_id=request.session.session_key)

    items_with_subtotal = items.annotate(sub_total=F('quantity') * F('serving__price'))
    total = items_with_subtotal.aggregate(total=Sum('sub_total'))['total']
    
    context = {'items': items_with_subtotal, 'total': total}
    return render(request, 'cart/cart.html', context)      


def update_cart(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    item = CartItem.objects.get(id=item_id)
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user.id)
        if action == 'remove':
            item.quantity -= 1
            item.save()
            response = {
                'item_qty': item.quantity,
                'sub_total': item.serving.price * item.quantity,
                'deleted': 'false',
                'total': sum(item.serving.price * item.quantity for item in items),
                'items_count': sum(item.quantity for item in items),
            }
            if item.quantity <= 0:
                item.delete()
                response = {
                    'item_qty': item.quantity,
                    'sub_total': item.serving.price * item.quantity,
                    'deleted': 'true',
                    'total': sum(item.serving.price * item.quantity for item in items),
                    'items_count': sum(item.quantity for item in items),
                }

        elif action == 'add':
            item.quantity += 1
            item.save()
            response = {
                'item_qty': item.quantity,
                'sub_total': item.serving.price * item.quantity,
                'deleted': 'false',
                'total': sum(item.serving.price * item.quantity for item in items),
                'items_count': sum(item.quantity for item in items),
            }

    else:
        cart = Cart(request)
        items = CartItem.objects.filter(session_id=request.session.session_key)
        if action == 'remove':
            item.quantity -= 1
            item.save()
            cart.update_item(item, item.serving, item.quantity)
            response = {
                'item_qty': item.quantity,
                'sub_total': item.serving.price * item.quantity,
                'deleted': 'false',
                'total': sum(item.serving.price * item.quantity for item in items),
                'items_count': sum(item.quantity for item in items),
            }
            if item.quantity <= 0:
                item.delete()
                response = {
                    'item_qty': item.quantity,
                    'sub_total': item.serving.price * item.quantity,
                    'deleted': 'true',
                    'total': sum(item.serving.price * item.quantity for item in items),
                    'items_count': sum(item.quantity for item in items),
                }

        elif action == 'add':
            item.quantity += 1
            item.save()
            cart.update_item(item, item.serving, item.quantity)
            response = {
                'item_qty': item.quantity,
                'sub_total': item.serving.price * item.quantity,
                'deleted': 'false',
                'total': sum(item.serving.price * item.quantity for item in items),
                'items_count': sum(item.quantity for item in items),
            }

    return JsonResponse(response)


def load_cart_count(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user.id)
        items_count = sum(item.quantity for item in items)
        response = {'items_count': items_count}
    else:
        items = CartItem.objects.filter(session_id=request.session.session_key)
        items_count = sum(item.quantity for item in items)
        response = {'items_count': items_count}
        
    return JsonResponse(response)


    
    
    