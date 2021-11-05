from django.contrib import admin
from .models import Brand, custom,Prodect,Catagory,ReviewRating
from panel import models

# Register your models here.

class CatagoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'cat_slug': ('cat_name')}
    list_display = ('cat_name', 'cat_slug')

class ProdectAdmin(admin.ModelAdmin):
    list_display = ('prodectname','price','stock','catagory','date','is_avilable')
    prepopulated_fields = {'slug': ('prodectname',)}


admin.site.register(custom)
admin.site.register(Prodect)
admin.site.register(Catagory)
admin.site.register(ReviewRating)
admin.site.register(Brand)
