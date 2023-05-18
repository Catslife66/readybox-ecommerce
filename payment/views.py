import stripe
import json

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404

from accounts.models import User, ShippingAddress
from cart.models import CartItem
from orders.models import Order, OrderItem
  

@login_required
def check_out(request):
    items = CartItem.objects.filter(user_id=request.user.id)
    qty_sum = items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    context = {'items': items, 'qty_sum': qty_sum}
    return render(request, 'payment/check_out.html', context)


@login_required
def payment_intent(request):
    items = CartItem.objects.filter(user_id=request.user.id)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    items_with_subtotal = items.annotate(sub_total=F('quantity') * F('serving__price'))
    total = items_with_subtotal.aggregate(total=Sum('sub_total'))['total']
    
    # convert total price to integer so stripe can process
    total = "{:.2f}".format(total)
    total = total.replace('.', '')
    total = int(total)

    # create a payment intent
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount = total,
        currency = 'gbp',
        metadata = {
            'userId': user_id,
        }
    )

    # when a payment intent created, create an order object
    try:
        user_order = Order.objects.get(order_key=intent.client_secret, user_id=user_id)
    except:
        user_order = Order.objects.create(user=user, total_amount=total, order_key=intent.client_secret)
    
    order_id = user_order.pk
    for item in items:
        order_item = OrderItem.objects.create(order_id=order_id, menu_id=item.menu.id, serving_id=item.serving.id, quantity=item.quantity, sub_price=item.serving.price)
    
    response = {
        'stripeKey': settings.STRIPE_PUBLIC_KEY,
        'clientSecret': intent.client_secret,
        'id': intent.id,
        'userid':user_id
        }
    return JsonResponse(response)


@login_required
def payment_update_shipping(request):
    data = json.loads(request.body)
    user_id = data['user_id']
    intent_id = data['id']
    full_name = data['full_name'] 
    email = data['email']
    address1 = data['address1']
    address2 = data['address2'] 
    city = data['city']
    postcode = data['postcode']
    mobile = data['mobile']
    order_key = data['client_secret']
    
    shipping = {
                'address1': address1,
                'address2': address2,
                'city': city,
                'postcode': postcode,
                }
    shipping_json = json.dumps(shipping)
    contact = {
                'email': email,
                'mobile': mobile
                }
    contact_json = json.dumps(contact)
    
    if request.user.id == user_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            intent_id,
            metadata={
                'recipient': full_name,
                'shipping': shipping_json,
                'contact': contact_json
            },
        )
        shipping_address = ShippingAddress.objects.create(user_id=user_id, full_name=full_name, email=email, address1=address1, address2=address2, postcode=postcode, town=city, contact_number=mobile)
        Order.objects.filter(order_key=order_key).update(shipping_id=shipping_address.id)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
    

def send_order_confirmation_email(user, order, order_items):
    subject = 'Your order confirmation'
    message = render_to_string('payment/order_confirmation_email.html', {'user':user, 'order': order, 'order_items': order_items})
    recipient_list = [user.email]
    send_mail(subject, message, recipient_list, html_message=message)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        order_key = event.data.object.client_secret
        order = Order.objects.filter(order_key=order_key)
        order.update(payment_status=True)
        send_mail(
            'Order Confirmation',
            'order is confirmed',
            'admin@host.com',
            ['a@a.com'],
            fail_silently=False,
        )
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


