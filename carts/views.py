from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.contrib import messages
from .models import Cart, Cart_item
from panel.models import Prodect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required



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
def remove_cart(request, id):
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
    return redirect('cart')

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

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request,'userst/checkout.html',context)







