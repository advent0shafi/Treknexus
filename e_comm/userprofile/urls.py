from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('address/',views.address,name='address'),
    path('user_address/',views.user_address,name='user_address'),
    path('add_address/',views.add_address,name='add_address'),
    path('edit_address/<int:address_id>',views.edit_address,name='edit_address'),
    path('profile_view/',views.profile_view,name='profile_view'),
     path('test/',views.test,name='test'),
]

