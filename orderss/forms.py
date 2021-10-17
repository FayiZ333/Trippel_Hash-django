from django import forms
from .models import Order,Adrs


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','phone2','email','address','country','state','city','district','pincode','order_note']



class AddressForm(forms.ModelForm):
    class Meta:
        model = Adrs
        fields = ['first_name','last_name','phone','phone2','email','adrs','country','state','city','district','pincode']

    def _init_(self, *args, **kwargs):
        super(AddressForm, self)._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


