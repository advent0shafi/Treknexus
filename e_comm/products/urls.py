from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
  

    path('product_details/<slug:slug>',views.product_details,name='product_details'),

    # path('search/',views.search,name="search"),

    path('shop/<int:category_id>',views.shop,name='shop'),

    path('filter/<int:category_id>',views.filter,name='filter'),

]

