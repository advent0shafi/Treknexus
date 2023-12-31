from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path('adminpage/',views.adminpage,name='adminpage'),

path('admin_home',views.admin_home,name='admin_home'),

path('admin_signin',views.admin_signin,name='admin_signin'),

path('userlist/',views.userlist,name='userlist'),

path('order_all/',views.order_all,name='order_all'),

path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

path('addproduct/',views.addproduct, name='addproduct'),

path('block/<int:user_id>/', views.block_user, name='block_user'),

path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),

path('catogery/',views.catogery, name='catogery'),

path('catogery_add/',views.catogery_add, name='catogery_add'),

 path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),

path('catogery_delete/<int:catogery_id>', views.catogery_delete, name='catogery_delete'),

path('product_view/<int:product_id>', views.product_view, name='product_view'),

path('variant_add/<int:product_id>',views.variant_add,name='variant_add'),

path(' variant_edit/<int:variant_id>',views.variant_edit,name='variant_edit'),

path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),

path('activate_product/<int:product_id>', views.activate_product, name='activate_product'),

path('order_views/<int:order_id>',views.order_views,name='order_views'),

path('coupon/',views.coupon_view,name="coupons"),

path('admin_logout/',views.admin_logout,name="admin_logout"),

path('coupon_expired/<int:coupon_id>',views.coupon_expired,name='coupon_expired'),

path('coupon_activate/<int:coupon_id>',views.coupon_activate,name='coupon_activate'),

path('sales_report/', views.sales_report, name='sales_report'),

path('banner_view/',views.banner_view, name="banner_view"),

path('banner_remove/<int:banner_id>',views.banner_remove,name='banner_remove'),

path('banner_active/<int:banner_id>',views.banner_active,name='banner_active'),

path('banner_block/<int:banner_id>',views.banner_block,name='banner_block'),

path('edit_banner/<int:banner_id>',views.edit_banner,name='edit_banner'),

path('detete_image/<int:image_id>',views.detete_image,name='detete_image'),

path('return_orders/',views.return_orders, name="return_orders"),

path('refund/<int:order_id>',views.refund,name='refund'),

]