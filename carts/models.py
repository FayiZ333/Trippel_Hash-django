from datetime import date
from django.db import models
from panel.models import Prodect, custom

# Create your models here.


class Cart(models.Model):
    cart_id             = models.CharField(max_length=333, blank=True)
    cart_date           = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart_id



class Cart_item(models.Model):
    user            = models.ForeignKey(custom, on_delete= models.CASCADE,null=True)
    prodect         = models.ForeignKey(Prodect, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)

    def sub_total(self):
        return self.prodect.price * self.quantity

    def __str__(self):
        return self.prodect




class BuynowItem(models.Model):
    user = models.ForeignKey(custom, on_delete=models.CASCADE, null=True)
    prodect = models.ForeignKey(Prodect, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.prodect.price * self.quantity

    def __str__(self):
        return str(self.prodect)
