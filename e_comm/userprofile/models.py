from django.db import models
from django.contrib.auth.models import User

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


    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"
