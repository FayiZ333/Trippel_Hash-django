from django.db import models
from django.db.models.fields import CharField, DateField, TextField, TimeField
from panel.models import Prodect,custom


# Create your models here.

class Wish_list(models.Model):
    prodect = models.ForeignKey(Prodect, on_delete=models.CASCADE)
    user = models.ForeignKey(custom, on_delete=models.CASCADE)

    
    def __str__(self) :
        return self.active