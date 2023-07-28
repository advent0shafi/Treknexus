from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from products.models import *
from django.db.models.signals import post_save

import string
import random

# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField( max_length=50)
    address_line_1 = models.CharField(max_length=250)
    address_line_2 = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField( max_length=254)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"



# Create your models here.

def generate_referral_code():
    # Implement a function to generate a unique referral code
    code_length = 6
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(code_length))


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=10, unique=True)
    referred_by = models.ForeignKey(User, related_name='referrals', null=True, blank=True, on_delete=models.SET_NULL)
    

    def str(self):
        return f"{self.user.username}'s Referral: {self.referral_code} Referred: {self.referred_by} "

    @receiver(post_save, sender=User)
    def create_user_wallet(sender, instance, created, **kwargs):
        if created:
            referral_code = generate_referral_code()
            Referral.objects.create(user=instance, referral_code=referral_code)