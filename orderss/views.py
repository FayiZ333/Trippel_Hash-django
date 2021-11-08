from django import forms
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from carts.models import BuynowItem, Cart_item,Cart
from coupons.models import  Coupons as Coupon, CouponCheck
from panel.models import Prodect
from .forms import OrderForm,AddressForm
import datetime
from .models import Adrs, Order, OrderProdect, Payment
import json

# Create your views here.

def pay(request):
    body = json.loads(request.body)
    order = Order.objects.get(user= request.user, is_ordered=False, order_number= body['orderID'])

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    if 'coupon_id' in request.session:
        coupon_id = request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        CouponCheck.objects.create(coupon=coupon, user=request.user)



    cart_items = Cart_item.objects.filter(user = request.user)

    for item in cart_items:
        orderprodect = OrderProdect()
        orderprodect.order_id = order.id
        orderprodect.payment = payment
        orderprodect.user_id = request.user.id
        orderprodect.prodect_id = item.prodect_id
        orderprodect.quantity = item.quantity
        orderprodect.prodect_price = item.prodect.price
        orderprodect.ordered = True
        orderprodect.save()

        ##########
        prodect = Prodect.objects.get(id=item.prodect_id)
        prodect.stock -= item.quantity
        prodect.save()


    Cart_item.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id, 
    }
    return JsonResponse(data)

    return render(request,'userst/payment.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items  = Cart_item.objects.filter(user = current_user)
    cart_count  = cart_items.count()
    if cart_count <= 0:
        return redirect('hom')


    pre_grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.prodect.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (3 * total)/100
    pre_grand_total = total + tax


    if 'coupon_id' in request.session:
        discount = request.session['discount_price']
        grand_total = request.session['grandtotal']
        
    else:
        discount = 0
        grand_total = pre_grand_total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.phone2 = form.cleaned_data['phone2']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.district = form.cleaned_data['district']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }

            return render(request,'userst/payment.html',context)
    else:
        return redirect('check_out')


def address(request):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            print('saved')
            return redirect(url)
        else:
            print('ddd')
    else:
        address_form = AddressForm()

    addresses = Adrs.objects.filter(user=request.user)

    context = {
        'address_form': address_form,
        'addresses': addresses,
    }

    return render(request, 'my_addresses.html', context)


# @login_required(login_url = 'signin')
def delete_address(request):
    address_id = request.POST['id']
    Adrs.objects.filter(id=address_id).delete()
    return JsonResponse({'success': True})

def success(request, ord_no, total=0):

    order = Order.objects.get(order_number=ord_no)
    order_prodects = OrderProdect.objects.filter(order_id=order.id)
    payment = Payment.objects.get(id=order.payment_id)

    for order_prodect in order_prodects:
        total = total + order_prodect.prodect_price

    context = {
        'order' : order,
        'order_prodects' : order_prodects,
        'total' : total,
        'payment':payment,
    }
    return render(request,'userst/success.html',context)



def buynow_place_order(request, total=0, quantity=0):
    current_user = request.user

    buynow_items = BuynowItem.objects.filter(user=current_user)
    cart_count  = buynow_items.count()
    if cart_count <= 0:
        return redirect('hom')


    pre_grand_total = 0
    tax = 0
    for buynow_item in buynow_items:
        total += (buynow_item.prodect.price * buynow_item.quantity)
        quantity += buynow_item.quantity
    tax = (3 * total)/100
    pre_grand_total = total + tax


    if 'coupon_id' in request.session:
        discount = request.session['discount_price']
        grand_total = request.session['grandtotal']
        
    else:
        discount = 0
        grand_total = pre_grand_total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.phone2 = form.cleaned_data['phone2']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.district = form.cleaned_data['district']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            
            context = {
                'order' : order,
                'buynow_items' : buynow_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }

            return render(request,'userst/buynow_payments.html',context)
    else:
        return redirect('check_out')


def buynow_payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user= request.user, is_ordered=False, order_number= body['orderID'])

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    if 'coupon_id' in request.session:
        coupon_id = request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        CouponCheck.objects.create(coupon=coupon, user=request.user)



    buynow_items = BuynowItem.objects.filter(user=request.user)

    for item in buynow_items:
        orderprodect = OrderProdect()
        orderprodect.order_id = order.id
        orderprodect.payment = payment
        orderprodect.user_id = request.user.id
        orderprodect.prodect_id = item.prodect_id
        orderprodect.quantity = item.quantity
        orderprodect.prodect_price = item.prodect.price
        orderprodect.ordered = True
        orderprodect.save()

        ##########
        prodect = Prodect.objects.get(id=item.prodect_id)
        prodect.stock -= item.quantity
        prodect.save()


    BuynowItem.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id, 
    }
    return JsonResponse(data)

