from django.db import models
from products.models import *
from userorder.models import *
from django.contrib.auth.models import User


# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_price = models.IntegerField(default=150)
    mininum_amount = models.IntegerField(default=750)
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return self.coupon_code
    
class Usercoupon(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    total_price = models.BigIntegerField()

