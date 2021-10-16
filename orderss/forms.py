from django import forms
from django.db import models
from django.forms import fields
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','phone2','email','address','country','state','city','district','pincode','order_note']