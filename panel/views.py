import os
from django.forms.fields import SplitDateTimeField
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import auth
from panel.models import Prodect, Catagory, ReviewRating, custom
from carts.models import Cart_item,Cart
from carts.views import _cart_id
from orderss.models import OrderProdect,Order
from django.db.models import Q
from .forms import ReviewForm

# Create your views here.

def adhom(request):
    earning = 0
    users   = custom.objects.all()
    prodects = Prodect.objects.all()
    catagorys = Catagory.objects.all()

    totals = OrderProdect.objects.filter(status = "Deliverd")

    for total in totals:
        earning += total.prodect_price

    context = {
        'users':users,
        'prodects':prodects,
        'catagorys':catagorys,
        'earning':earning,

    }
    return render(request, 'adm/index.html',context)

def prolist(request):
    prodects = Prodect.objects.all().order_by('id')
    return render(request, 'adm/proList.html',{'prodects':prodects})

def proadd(request):
    if request.method == "POST":
        brand           = request.POST['brand']
        prodectname     = request.POST['prodectname']
        model_no        = request.POST['model_no']
        gender          = request.POST['gender']
        catagory        = Catagory.objects.get(id=request.POST['catagory'])
        price           = request.POST['price']
        stock           = request.POST['stock']
        discription     = request.POST['discription']
        img1            = request.FILES['img1']
        img2            = request.FILES['img2']
        img3            = request.FILES['img3']
        slug = prodectname.lower().replace(" ","-")

        
        
        if Prodect.objects.filter(prodectname=prodectname).exists():
            messages.info(request,'Prodect name is alredy taken!!!')
            return redirect('/proadd')
        elif Prodect.objects.filter(model_no=model_no).exists():
            messages.info(request,'model number is alredy taken!!!')
            return redirect('/proadd')
        else:
            prodects = Prodect(model_no=model_no, brand=brand, prodectname=prodectname, gender=gender, catagory=catagory,
            price=price, stock=stock, discription=discription, img1=img1, img2=img2, img3=img3, slug=slug)
            prodects.save()
        
            return redirect('prolist')
        
    else:
        return render(request, 'adm/proAdd.html')

def delete(request):
    id = request.POST['id']

    Prodect.objects.filter(id=id).delete()
    return JsonResponse({'success': True})

def edit(request, id):
    prodect = Prodect.objects.get(id=id)
    
    if request.method == 'POST':
        
        if len(request.FILES) != 0:
            if len(prodect.img1) > 0:
                os.remove(prodect.img1.path)
            prodect.img1            = request.FILES['img1']
            
            if len(prodect.img2) > 0:
                os.remove(prodect.img2.path)
            prodect.img2            = request.FILES['img2']

            if len(prodect.img3) > 0:
                os.remove(prodect.img3.path)
            prodect.img3            = request.FILES['img3']

        brand           = request.POST.get('brand')
        prodectname     = request.POST.get('prodectname')
        model_no        = request.POST.get('model_no')
        gender          = request.POST.get('gender')
        catagory        = Catagory.objects.get(cat_name=request.POST['catagory'])
        price           = request.POST.get('price')
        stock           = request.POST.get('stock')
        discription     = request.POST.get('discription')
        slug = prodectname.lower().replace(" ","-")
        # # os.remove(prodect.img1.path)
        # prodect.img1            = request.FILES.get('img1')
        # # os.remove(prodect.img2.path)
        # prodect.img2            = request.FILES.get('img2')
        # # os.remove(prodect.img3.path)
        # prodect.img3            = request.FILES.get('img3')
        
        if Prodect.objects.exclude(id=id).filter(prodectname=prodect.prodectname).exists():
            messages.error(request,'Prodect name is already taken!')
            return render(request,'adm/edit.html',{'id':id})

        elif Prodect.objects.exclude(id=id).filter(model_no=prodect.model_no).exists():
            messages.error(request,'model_no is already taken!')
            return render(request,'adm/edit.html',{'id':id})

        else:
            prodect = Prodect.objects.filter(id=id).update(model_no=model_no, brand=brand, prodectname=prodectname, gender=gender, catagory=catagory,
            price=price, stock=stock, discription=discription, slug=slug, img3=prodect.img3, img2=prodect.img2, img1=prodect.img1)
            return redirect('prolist')

    else:
        context = {'prodect':prodect}
        return render(request,'adm/edit.html',context) 



def cat_add(request):
    if request.method == 'POST':

        cat_name                = request.POST['cat_name']
        cat_discription         = request.POST['cat_discription']
        cat_date                = request.POST['cat_date']
        cat_img                 = request.FILES['cat_img']
        cat_slug                = cat_name.lower().replace("","-")

        if Catagory.objects.filter(cat_name=cat_name).exists():
            messages.info(request,'Catagory name is alredy taken!!!')
            return redirect('/cat_add')
        else:
            catagory = Catagory(cat_name=cat_name, cat_discription=cat_discription, cat_date=cat_date, cat_img=cat_img, cat_slug=cat_slug)

            catagory.save()
            return redirect('cat_list')

    else:
        return render(request,'adm/cat_add.html')

        
def cat_list(request):
    catagorys = Catagory.objects.all().order_by('id')
    return render(request, 'adm/cat_list.html',{'catagorys':catagorys})

def cat_delete(request, id):
    
    Catagory.objects.filter(id=id).delete()
    return redirect('cat_list')



def user_list(request):
    users = custom.objects.all().order_by('id')
    return render(request, 'adm/user_list.html',{'users':users})


def block(request,id):
    user = custom.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('user_list')

def unblock(request,id):
    user = custom.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('user_list')

def blocked_users(request):
    users = custom.objects.all().order_by('id').filter(is_active=False)
    return render(request, 'adm/user_list.html',{'users':users})


def order_list(request):
    order_prodects = OrderProdect.objects.all().order_by("-created_at")
    context = {
        'order_prodects': order_prodects,
    }
    return render(request,'adm/orderlist.html',context)


def order_ststus(request, order_id):

    status = request.POST['status']
    if status == 'Cancelled':

        cancel_order = OrderProdect.objects.get(id=order_id)
        Prodect.objects.filter(id=cancel_order.prodect.id).update(stock=cancel_order.prodect.stock + cancel_order.quantity)
        OrderProdect.objects.filter(id=order_id).update(status="Cancelled")

    elif status == 'Return':

        cancel_order = OrderProdect.objects.get(id=order_id)
        Prodect.objects.filter(id=cancel_order.prodect.id).update(stock=cancel_order.prodect.stock + cancel_order.quantity)
        OrderProdect.objects.filter(id=order_id).update(status="Return")

    else:
        orderststus = OrderProdect.objects.filter(id=order_id).update(status=status)

    return redirect('order_list')


def order_history(request):
    order_historys = OrderProdect.objects.filter(Q(status='Deliverd') | Q(status='Canceled')).order_by('-created_at')
    context = {
        'order_historys': order_historys,
    }
    return render(request,'adm/order_history.html',context)


def submit_review(request, prodect_id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id= request.user.id, prodect__id= prodect_id)
            form = ReviewForm(request.POST, instance= reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.prodect_id = prodect_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)

