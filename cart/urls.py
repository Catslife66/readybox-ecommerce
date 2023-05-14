from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('cart_count/', views.load_cart_count, name='cart_count'),
   
]