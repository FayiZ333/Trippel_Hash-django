from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import activate
from .models import Coupons as Coupon,CouponCheck
from django.http.response import JsonResponse
from .forms import CouponForm
from django.contrib import messages
from datetime import date
from django.db.models import Q


# Create your views here.

def checkCoupon(request, discount=0):
    
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        del request.session['grandtotal']
        del request.session['discount_price']
        
    flag = 0
    discount_price = 0
    coupon = request.POST['coupon']
    total = float(request.POST['total'])
    if Coupon.objects.filter(code=coupon).exists():
        coup = Coupon.objects.get(code=coupon)
        if coup.status == True:
            flag = 1
            if not CouponCheck.objects.filter(user=request.user, coupon=coup):
                discount = total-(total*int(coup.discount)/100)
                discount_price = total*int(coup.discount)/100
                flag = 2
                request.session['grandtotal'] = discount
                request.session['discount_price'] = discount_price
                request.session['coupon_id'] = coup.id
    data = {
        
        'total': discount,
        'flag': flag,
        'discount_price': discount_price,

    }
    return JsonResponse(data)

#Coupon Management
def admin_coupon(request):
    form = CouponForm()
    today = date.today()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            form.save()
            coupon = Coupon.objects.get(code=code)

            if coupon.valid_from <= today and coupon.valid_to >= today:

                Coupon.objects.filter(id=coupon.id).update(status=True)

            else:
                Coupon.objects.filter(id=coupon.id).update(status=False)

            messages.info(request, "1 Coupon Added Successfully")
            return redirect('admin_coupon_list')
    context = {'form': form}
    return render(request, "adm/new_coupon.html", context)


def admin_coupon_list(request):
    coupon = Coupon.objects.all()
    today = date.today()
    for coup in coupon:

        if coup.valid_from <= today and coup.valid_to >= today:

            Coupon.objects.filter(id=coup.id).update(status=True)
        else:
            
            Coupon.objects.filter(id=coup.id).update(status=False)

    context = {'coupon': coupon}
    return render(request, 'adm/coupon_list.html', context)


def coupon_edit(request, id):
    qs = get_object_or_404(Coupon, id=id)
    today = date.today()
    form = CouponForm(instance=qs)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=qs)
        print(qs.valid_from)
        if form.is_valid():
            form.save()
            if qs.valid_from <= today and qs.valid_to >= today:

                Coupon.objects.filter(id=qs.id).update(status=True)
                print(qs.status)
            else:
                
                Coupon.objects.filter(id=qs.id).update(status=False)
                print(qs.status)


            messages.info(request, "1 Coupon Edited Successfully")
            return redirect('admin_coupon_list')
    context = {'form': form}
    return render(request, 'adm/admin_coupon_edit.html', context)


def coupon_delete(request):
    id = request.POST['id']

    coupon_delete = Coupon.objects.get(id=id)
    coupon_delete.delete()
    return JsonResponse({'success': True})
