from django.db import models
from django.contrib.auth.models import User
from products.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class whishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Variant,on_delete=models.CASCADE ,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_user_wallet(sender, instance, created, **kwargs):
        if created:
            whishlist.objects.create(user=instance)