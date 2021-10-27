from django.contrib import admin
from .models import BuynowItem, Cart, Cart_item

# Register your models here.

admin.site.register(Cart)
admin.site.register(BuynowItem)
admin.site.register(Cart_item)