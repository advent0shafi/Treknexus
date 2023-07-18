from django.db import models
from django.contrib.auth.models import User
from products.models import *

# Create your models here.
class whishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Variant,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    