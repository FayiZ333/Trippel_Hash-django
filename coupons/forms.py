from django import forms
from django.forms import fields, models
from .models import CouponCheck,Coupon


#coupon
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'status']