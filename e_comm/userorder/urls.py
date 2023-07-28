from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
      path('checkout/<int:address_id>',views.checkout,name='checkout'),
      
      path('online_payment_order/<userId>',views.online_payment_order,name='online_payment_order'),

      path('place_order/<userId>',views.place_order,name='place_order'),

      path('pay_wallet/<userId>',views.pay_wallet,name='pay_wallet'),

      path('ordertable',views.ordertable,name="ordertable"),

      path('order_view/<int:order_id>',views.order_view,name='order_view'),

      path('cancel_orders/<int:order_id>/', views.cancel_orders, name='cancel_orders'),
      path('return_order/<int:order_id>/', views.return_order, name='return_order'),


      path('initiate_payment/', views.initiate_payment, name='initiate_payment'),

      path('order_success/<int:orderId>/', views.order_success, name='order_success'),\
      
      path('order_pdf/<int:order_id>/', views.order_pdf, name='order_pdf'),

      
     
]

