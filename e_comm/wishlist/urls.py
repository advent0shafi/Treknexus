from django.contrib import admin
from django.urls import path,include
from . import views



urlpatterns = [

    path('wishlist', views.wishlist, name='wishlist'),
    path('adding_wishlist/', views.adding_wishlist, name='adding_wishlist'),
    path('removing_wishlist/', views.removing_wishlist, name='removing_wishlist'),
    path('remove_item/<int:variant_id>', views.remove_item, name='remove_item'),

]
