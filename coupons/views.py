from django.shortcuts import redirect, render, get_object_or_404
from .models import Coupon,CouponCheck
from django.http.response import JsonResponse
from .forms import CouponForm
from django.contrib import messages


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
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "1 Coupon Added Successfully")
            return redirect('admin_coupon_list')
    context = {'form': form}
    return render(request, "adm/new_coupon.html", context)


def admin_coupon_list(request):
    coupon = Coupon.objects.all()
    context = {'coupon': coupon}
    return render(request, 'adm/coupon_list.html', context)


def coupon_edit(request, id):
    qs = get_object_or_404(Coupon, id=id)
    form = CouponForm(instance=qs)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=qs)
        if form.is_valid():
            form.save()
            messages.info(request, "1 Coupon Edited Successfully")
            return redirect('admin_coupon_list')
    context = {'form': form}
    return render(request, 'adm/admin_coupon_edit.html', context)


def coupon_delete(request):
    id = request.POST['id']

    coupon_delete = Coupon.objects.get(id=id)
    coupon_delete.delete()
    return JsonResponse({'success': True})
