from django.db import models
from products.models import Category

# Create your models here.
class Banner(models.Model):
    name = models.CharField (max_length=200)
    banner_image = models.ImageField(upload_to='Banner')
  
  