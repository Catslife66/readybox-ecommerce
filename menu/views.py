from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db.models import Q

from .models import Menu, Serving
from cart.models import Cart, CartItem
from cart.cart import Cart


def menu_list(request):
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, 'menu/menu_list.html', context)


def menu_detail(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    servings = menu.servings.all()
    context = {'menu': menu, 'servings': servings}
    if request.htmx:
        return render(request, 'menu/menu_detail_modal.html', context)
    else:
        return render(request, 'menu/menu_detail.html', context)
    

def add_to_cart(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    serving_id = request.POST.get('serving_id')
    serving = Serving.objects.get(id=serving_id)
    item_qty = int(request.POST.get('item_qty'))
    response = {
        'slug': slug,
        'serving_id': serving_id,
        'item_qty': item_qty,
    }
    if request.user.is_authenticated:

        item = CartItem.objects.filter(Q(user_id=request.user.id) & Q(menu=menu) & Q(serving=serving))

        if item:
            for i in item:
                if item_qty == 0:
                    i.quantity += 1
                else:
                    i.quantity += item_qty
                i.save()
        else:
            new_item = CartItem.objects.create(user_id=request.user.id, menu=menu, serving=serving)
            if item_qty == 0:
                new_item.quantity = 1
            else:
                new_item.quantity = item_qty
            new_item.save()

        items = CartItem.objects.filter(user_id=request.user.id)

        response = {
                'slug': slug,
                'items_count': sum(item.quantity for item in items),
                }
    else:
        cart = Cart(request)
        item = CartItem.objects.filter(Q(session_id=request.session.session_key) & Q(menu=menu) & Q(serving=serving))
        if item:
            for i in item:
                if item_qty == 0:
                    i.quantity += 1
                else:
                    i.quantity += item_qty
                i.save()
                cart.update_item(i, serving, i.quantity)

        else:
            new_item = CartItem.objects.create(session_id=request.session.session_key, menu=menu, serving=serving)
            if item_qty == 0:
                new_item.quantity = 1
            else:
                new_item.quantity = item_qty
            new_item.save()
            cart.update_item(new_item, serving, new_item.quantity)
        
        items = CartItem.objects.filter(session_id=request.session.session_key)
        
        response = {
            'slug': slug,
            'items_count': sum(item.quantity for item in items),
        }

    return JsonResponse(response)


def search(request):
    query = request.GET.get('q')
    obj_lists = Menu.objects.search(query).distinct()
    context = {'obj_lists': obj_lists}
    return render(request, 'menu/search_result.html', context)