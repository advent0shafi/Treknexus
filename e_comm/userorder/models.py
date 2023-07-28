from django.db import models
from userprofile.models import UserAddress
from products.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid

# # Create your models here.



class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('PAID','Paid'),
        ('CANCELLED','Cancelled'),
        ('REFUNDED','Refunded'),
      
    ]
    ORDER_STATUS_CHOICES = [
        ('CANCELLED','Cancelled'),
        ('DELIVERED','Delivered'),
        ('ORDERED','Ordered'),
        ('RETURNED','Returned'),
        ('SHIPPED','Shipped'),
        ('PENDING','Pending'),
        ('PROCESSING','Processing'),

    ]
    PAYMENT_METHOD_CHOICES = [
        ('PAYPAL', 'PayPal'),
        ('CASH_ON_DELIVERY', 'Cash on Delivery'),
        ('RAZORPAY', 'RazorPay'),
        ('WALLET', 'Wallet'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='ordered')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    order_status =  models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='ordered',null=True,blank =True)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)
    razor_pay_order_id =models.CharField( max_length=150,null=True, blank=True)
    razor_pay_payment_id =models.CharField( max_length=150,null=True, blank=True)
    razor_pay_payment_signature =models.CharField( max_length=150,null=True, blank=True)

    def __str__(self):
        return f"{self.id, self.tracking_no}"
    def _str_(self):
        return f"{self.id}  {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_date:
            self.order_date = timezone.now()  # Set the order date to the current time if it's not set
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(hours=24)
        super().save(*args, **kwargs)
   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    def __str__(self):
        return f"{self.order.id, self.order.tracking_no}"
         
    