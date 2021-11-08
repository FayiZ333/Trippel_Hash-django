from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, JsonResponse
from django.contrib import messages
from .models import BuynowItem, Cart, Cart_item
from panel.models import Prodect, custom
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from orderss.models import Adrs
from datetime import date
from coupons.models import Coupons as Coupon



# Create your views here.

@login_required(login_url='login')
def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(
                user=request.user, is_active=True).order_by('-id')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_item.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.prodect.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'userst/cart.html', context)

@login_required(login_url='login')
def remove_cart(request):
    id = request.POST['id']
    
    prodect = get_object_or_404(Prodect, id=id)
    try:
        if request.user.is_authenticated:
            cart_item = Cart_item.objects.get(prodect=prodect, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cart_item.objects.get(prodect=prodect, cart=cart)
        if cart_item.quantity > 1:
            if cart_item.prodect_id > 1:
                cart_item.quantity -= 1
                cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return JsonResponse({'success': True})

@login_required(login_url='login')
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='login')
def add_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    prodect = Prodect.objects.get(id=id)

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
        try:
            cart_item = Cart_item.objects.get(prodect=prodect, user=current_user)
            if cart_item.prodect_id < prodect.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.info(request,'No Much Stock!!!')

        except Cart_item.DoesNotExist:
            cart_item = Cart_item.objects.create(
                prodect=prodect,
                quantity=1,
                user=current_user,
            )
            cart_item.save()

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        try:
            cart_item = Cart_item.objects.get(prodect=prodect, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except Cart_item.DoesNotExist:
            cart_item = Cart_item.objects.create(
                prodect=prodect,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
    return redirect(url)


def add_item(request):
    id = request.POST['id']

    current_user = request.user
    prodect = Prodect.objects.get(id=id)

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
        try:
            cart_item = Cart_item.objects.get(prodect=prodect, user=current_user)
            if cart_item.quantity < prodect.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.info(request,'No More Stock!!!')

        except Cart_item.DoesNotExist:
            cart_item = Cart_item.objects.create(
                prodect=prodect,
                quantity=1,
                user=current_user,
            )
            cart_item.save()

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        try:
            cart_item = Cart_item.objects.get(prodect=prodect, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except Cart_item.DoesNotExist:
            cart_item = Cart_item.objects.create(
                prodect=prodect,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
    return JsonResponse({'success': True})


@login_required(login_url='login')
def remove_cart_item(request, id):
    prodect = get_object_or_404(Prodect, id=id)
    if request.user.is_authenticated:
        cart_item = Cart_item.objects.get(prodect=prodect, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cart_item.objects.get(prodect=prodect, cart=cart)    
    cart_item.delete()
    return redirect('cart')


    # def delete(request):
    # id = request.POST['id']
    # Category.objects.filter(id=id).delete()
    # return JsonResponse({'success':True})



@login_required(login_url='login')
def check_out(request, total=0, quantity=0, cart_items=None):

    today = date.today()
    coupon = Coupon.objects.all()
    for coup in coupon:

        if coup.valid_from <= today and coup.valid_to >= today:

            Coupon.objects.filter(id=coup.id).update(status=True)
        else:
            
            Coupon.objects.filter(id=coup.id).update(status=False)

    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        del request.session['grandtotal']
        del request.session['discount_price']

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_item.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.prodect.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    addresses = Adrs.objects.filter(user=request.user)
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'addresses':addresses,
    }
    return render(request,'userst/checkout.html',context)


@login_required(login_url='login')
def buy_now(request,id,tax=0, total=0, quantity=0, cart_items=None):
    BuynowItem.objects.all().delete()
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        del request.session['grandtotal']
        del request.session['discount_price']
    
    prodect = Prodect.objects.get(id=id)
    try:
        # get the cart using the cart id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        buynow_item = BuynowItem.objects.get(prodect=prodect, user=request.user)
        if buynow_item.quantity > buynow_item.prodect.stock-1:
            messages.info(request, 'Prodect Out of Stock')
            return redirect('cart')
        else:
            buynow_item.quantity += 1
            buynow_item.save()


    except BuynowItem.DoesNotExist:
        buynow_item = BuynowItem.objects.create(
            prodect=prodect,
            quantity=1,
            user=request.user,
        )
        buynow_item.save()


    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            buynow_items = BuynowItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            buynow_items = BuynowItem.objects.filter(cart=cart, is_active=True)
        for buynow_item in buynow_items:
            total += (buynow_item.prodect.price * buynow_item.quantity)
            quantity += buynow_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignore

    addresses = Adrs.objects.filter(user=request.user)

    context = {
        'total': total,
        'quantity': quantity,
        'buynow_items': buynow_items,
        'tax': tax,
        'grand_total': grand_total,
        'addresses': addresses,
    }
    return render(request, 'userst/buy_now_checkout.html', context)




