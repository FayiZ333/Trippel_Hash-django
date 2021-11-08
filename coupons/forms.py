from django import forms
from django.forms import fields, models
from .models import CouponCheck, Coupons as Coupon


#coupon

class DateInput(forms.DateInput):
    input_type = 'date'
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount','valid_to','valid_from']
        widgets = {
            'valid_from': DateInput(),
            'valid_to': DateInput(),
        }