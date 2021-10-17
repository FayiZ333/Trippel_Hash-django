from django.db import models
from panel.models import custom
from panel.models import Prodect

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(custom, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)   #total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def str(self):
        return self.payment_id



class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted','Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(custom, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, )
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Placed')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address} {self.address2}'

    def str(self):
        return self.full_name()
    # def _str_(self):
    #     return self.first_name


class OrderProdect(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(custom, on_delete=models.CASCADE)
    prodect = models.ForeignKey(Prodect, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    prodect_price = models.FloatField()
    status = models.CharField(max_length=10, default='Placed')
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def str(self):
        return self.prodect.prodectname


class Ex_Address(models.Model):
    user = models.ForeignKey(custom, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, )
    email = models.EmailField(max_length=50)
    address2 = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def str(self):
        return self.full_name()



class Adrs(models.Model):
    user = models.ForeignKey(custom, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, )
    email = models.EmailField(max_length=50)
    adrs = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def str(self):
        return self.full_name()