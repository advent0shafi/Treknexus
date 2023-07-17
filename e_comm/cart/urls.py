
from django.urls import path,include

from . import views

urlpatterns = [
    path('add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.view_cart, name='cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity', views.update_quantity, name='update_quantity'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    path('wallet', views.view_wallet, name='wallet'),
]