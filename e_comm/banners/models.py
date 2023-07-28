from django.db import models
from products.models import Variant

# Create your models here.
class Banner(models.Model):
    name = models.CharField (max_length=200)
    variants = models.ForeignKey(Variant,on_delete=models.CASCADE,blank=True,null=True)
    banner_image = models.ImageField(upload_to='Banner')
    is_active = models.BooleanField(default=True)
  