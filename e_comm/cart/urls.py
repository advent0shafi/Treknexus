
from django.urls import path,include

from . import views

urlpatterns = [
    path('add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart', views.view_cart, name='cart'),

    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('update_quantity', views.update_quantity, name='update_quantity'),

    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),

    path('wallet', views.view_wallet, name='wallet'),

    # path('add_to_guest_cart/<int:variant_id>/', views.add_to_guest_cart, name='add_to_guest_cart'),

    # path('guest_cart_view', views.guest_cart_view, name='guest_cart_view'),

    # path('remove_cart_item/<int:carts_id>/', views.remove_cart_item, name='remove_cart_item'),
    
    # path('update_guestcart_quantity', views.update_guestcart_quantity, name='update_guestcart_quantity'),
    
   
]