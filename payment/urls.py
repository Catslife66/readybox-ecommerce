from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('check-out/', views.check_out, name='check_out'),
    path('create-payment-intent/', views.payment_intent, name='payment_intent'),
    path('webhook/', views.stripe_webhook_view, name='stripe_webhook'),
    path('update_shipping/', views.payment_update_shipping, name='update_shipping'),
]