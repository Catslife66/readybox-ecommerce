from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_view, name='orders'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('orderplaced/', views.order_placed, name='order_placed'),
]
