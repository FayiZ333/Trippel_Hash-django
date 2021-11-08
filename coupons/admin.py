from django.contrib import admin
from .models import  Coupons as Coupon,CouponCheck

# Register your models here.

admin.site.register(Coupon)
admin.site.register(CouponCheck)

