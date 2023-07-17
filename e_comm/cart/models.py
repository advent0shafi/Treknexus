from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from products.models import *
from django.db.models import Sum
from decimal import Decimal
from coupon.models import Coupon
from django.db.models.signals import post_save

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupons = models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.CASCADE)
    
    @receiver(post_save, sender=User)
    def create_user_cart(sender, instance, created, **kwargs):
        if created:
            Cart.objects.create(user=instance)

    def __str__(self):
        return f"Cart #{self.pk} for {self.user.username}"

    def get_total_price(self):
        return self.cartitems_set.aggregate(total_price=Sum('price'))['total_price']

class CartItems(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField( max_digits=8, decimal_places=2)



    def get_item_price(self):
        return Decimal(self.price) * Decimal(self.quantity)
    
# User wallet 

class wallet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wallet_total =models.IntegerField(null=True,blank=True)


    @receiver(post_save, sender=User)
    def create_user_wallet(sender, instance, created, **kwargs):
        if created:
            wallet.objects.create(user=instance)
