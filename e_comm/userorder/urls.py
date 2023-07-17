from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
      path('checkout/<int:address_id>',views.checkout,name='checkout'),
      
      path('online_payment_order/<userId>',views.online_payment_order,name='online_payment_order'),

      path('place_order/<userId>',views.place_order,name='place_order'),

      path('ordertable',views.ordertable,name="ordertable"),

      path('order_view/<int:order_id>',views.order_view,name='order_view'),

      path('cancel_orderss/<int:order_id>/', views.cancel_orderss, name='cancel_orderss'),

      path('initiate_payment/', views.initiate_payment, name='initiate_payment'),

      path('order_success/<int:orderId>/', views.order_success, name='order_success'),
      
      # path('success/', views.success_view, name='success'),
]

