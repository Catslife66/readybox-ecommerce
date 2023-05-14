from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('search/', views.search, name='search'),
    path('<str:slug>/', views.menu_detail, name='menu_detail'), 
    path('<str:slug>/add/', views.add_to_cart, name='add_to_cart'), 
]