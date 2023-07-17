from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField( max_length=150)
    image = models.ImageField(upload_to='Category')
    slug = models.SlugField(unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE,default=1)
    descriptions = models.TextField(default='', blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True,null=True)
    is_avaiable = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products,self).save(*args, **kwargs)
    def __str__(self):
        return self.name
  


class color(models.Model):
    color = models.CharField( max_length=50)
    def __str__(self):
        return str(self.color)



class size(models.Model):
    size = models.CharField( max_length=50)  
    def __str__(self):
        return str(self.size)


class Variant(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey("Products", on_delete=models.CASCADE)
    size = models.ForeignKey("size", on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey("color", on_delete=models.CASCADE, null=True, blank=True)
    variant_image = models.ImageField( upload_to="Varients", height_field=None, width_field=None, max_length=None)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField( max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Variant, self).save(*args, **kwargs)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):

        return reverse("product_details", kwargs={"slug": self.slug})
    
class product_image(models.Model):
    product = models.ForeignKey("Variant",on_delete=models.CASCADE)
    image = models.ImageField( upload_to="products")