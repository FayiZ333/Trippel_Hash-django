import os
from django.forms.fields import SplitDateTimeField
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import auth
from panel.models import Brand, Prodect, Catagory, ReviewRating, custom
from carts.models import Cart_item,Cart
from carts.views import _cart_id
from orderss.models import OrderProdect,Order
from django.db.models import Q, Count
from .forms import ReviewForm
import datetime,calendar
from django.db.models.functions.datetime import ExtractMonth

# Create your views here.
def admin_login(request):
    if request.method == "POST":
        email = request.POST['login']
        password = request.POST['password']
        users =  auth.authenticate(email=email,password=password)
        print(users)
        if users is not None:
            if users.is_superuser == True:
                request.session['login'] = 'login'
                return JsonResponse({'success': True})
            else:
                context = {
                    'success': False,
                }
                return JsonResponse(context)
        else:
            context = {
                'success': False,
            }
            return JsonResponse(context)
    else:
        context = {
            'success': False,
        }
        return JsonResponse(context)

def admin_logout(request):
    del request.session['login']   
    return redirect('adhom')

def adhom(request):
    if request.session.has_key('login'):
        Placed = 0
        Shipping = 0
        Deliverd = 0
        Cancelled = 0
        Return = 0
        earning = 0
        users   = custom.objects.all()
        prodects = Prodect.objects.all().order_by('-id')[:5]
        catagorys = Catagory.objects.all().order_by('-id')[:5]

        totals = OrderProdect.objects.filter(status = "Deliverd")


        labels1 = []
        data1 = []
        orders=OrderProdect.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
        labels1=['jan','feb','march','april','may','june','july','august','september',]
        data1=[0,0,0,0,0,0,0,0,0]
        for d in orders:
            labels1.append(calendar.month_name[d['month']])
            data1.append([d['count']])




        for total in totals:
            earning += total.prodect_price


        order_prodects = OrderProdect.objects.all()

        for order_prodect in order_prodects:
            if order_prodect.status == "Placed":
                Placed += 1
            elif order_prodect.status == "Shipping":
                Shipping += 1
            elif order_prodect.status == "Deliverd":
                Deliverd += 1
            elif order_prodect.status == "Cancelled":
                Cancelled += 1
            elif order_prodect.status == "Return":
                Return += 1

        labels = ["Placed","Shipping","Deliverd","Cancelled","Return"]
        datas = [Placed,Shipping,Deliverd,Cancelled,Return]

        order_prodects = OrderProdect.objects.all().order_by('-id')[:5]

        context = {
            'Deliverd':Deliverd,
            'users':users,
            'prodects':prodects,
            'catagorys':catagorys,
            'earning':earning,
            'labels':labels,
            'datas':datas,
            'labels1':labels1,
            'data1':data1,
            'order_prodects':order_prodects,

        }
        return render(request, 'adm/index.html',context)
    else:
        return redirect('hom')

    

def prolist(request):
    prodects = Prodect.objects.all().order_by('-id')
    return render(request, 'adm/proList.html',{'prodects':prodects})

def proadd(request):
    if request.method == "POST":
        brand           = Brand.objects.get(id=request.POST['brand'])
        prodectname     = request.POST['prodectname']
        model_no        = request.POST['model_no']
        gender          = request.POST['gender']
        catagory        = Catagory.objects.get(id=request.POST['catagory'])
        price           = int(request.POST['price'])
        stock           = request.POST['stock']
        discription     = request.POST['discription']
        img1            = request.FILES['img1']
        img2            = request.FILES['img2']
        img3            = request.FILES['img3']
        slug = prodectname.lower().replace(" ","-")

        if request.POST['offer']:
            offer           = int(request.POST['offer'])


        if Prodect.objects.filter(prodectname=prodectname).exists():
            messages.error(request,'Prodect name is alredy taken!!!')
            return redirect('proadd')
        elif Prodect.objects.filter(model_no=model_no).exists():
            messages.error(request,'model number is alredy taken!!!')
            return redirect('proadd')
        else:
            if request.POST['offer'] and offer > 0:
                actual_price = price
                price = actual_price-(actual_price*offer/100)
                prodects = Prodect(model_no=model_no, brand=brand, prodectname=prodectname, gender=gender, catagory=catagory,
                price=price, stock=stock, discription=discription, img1=img1, img2=img2, img3=img3, slug=slug,offer=offer,actual_price=actual_price)
                prodects.save()
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
        
        if request.FILES.get('img1'):
            prodect.img1            = request.FILES['img1']
        if request.FILES.get('img2'):
            prodect.img2            = request.FILES['img2']
        if request.FILES.get('img3'):
            prodect.img3            = request.FILES['img3']

        prodect.brand           = request.POST['brand']
        prodect.prodectname     = request.POST['prodectname']
        prodect.model_no        = request.POST['model_no']
        prodect.gender          = request.POST['gender']
        prodect.catagory        = Catagory.objects.get(cat_name=request.POST['catagory'])
        prodect.price           = int(request.POST['price'])
        prodect.stock           = request.POST['stock']
        prodect.discription     = request.POST['discription']
        prodect.slug = prodect.prodectname.lower().replace(" ","-")
        if request.POST['offer']:
            prodect.offer           = int(request.POST['offer'])
        if request.POST['offer'] and prodect.offer > 0:
            prodect.actual_price = prodect.price
            prodect.price = prodect.actual_price-(prodect.actual_price*prodect.offer/100)
        
        if Prodect.objects.exclude(id=id).filter(prodectname=prodect.prodectname).exists():
            messages.error(request,'Prodect name is already taken!')
            return render(request,'adm/edit.html',{'id':id})

        elif Prodect.objects.exclude(id=id).filter(model_no=prodect.model_no).exists():
            messages.error(request,'model_no is already taken!')
            return render(request,'adm/edit.html',{'id':id})

        else:
            prodect.save()
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

def cat_edit(request, id):
    catagory = Catagory.objects.get(id=id)

    if request.method == 'POST':

        if request.FILES.get('cat_img'):
            catagory.cat_img            = request.FILES['cat_img']

        catagory.cat_name                = request.POST['cat_name']
        catagory.cat_discription         = request.POST['cat_discription']
        catagory.cat_date                = request.POST['cat_date']
        catagory.cat_slug                = catagory.cat_name.lower().replace("","-")

        if Catagory.objects.exclude(id=id).filter(cat_name=catagory.cat_name).exists():
            messages.info(request,'Catagory name is alredy taken!!!')
            return render(request, 'adm/cat_edit.html',{'id':id})
        else:
            catagory.save()
            return redirect('cat_list')
    else:
        context = {
            'catagory':catagory,
        }
        return render(request, 'adm/cat_edit.html',context)

        
def cat_list(request):
    catagorys = Catagory.objects.all().order_by('-id')
    return render(request, 'adm/cat_list.html',{'catagorys':catagorys})

def cat_delete(request,id):
    print(id)
    Catagory.objects.filter(id=id).delete()
    return redirect('cat_list')

def user_list(request):
    users = custom.objects.all().order_by('id')
    return render(request, 'adm/user_list.html',{'users':users})


def block(request):
    id = request.POST['id']

    user = custom.objects.get(id=id)
    user.is_active=False
    user.save()
    return JsonResponse({'success': True})

def unblock(request):
    id = request.POST['id']

    user = custom.objects.get(id=id)
    user.is_active=True
    user.save()
    return JsonResponse({'success': True})

def blocked_users(request):
    users = custom.objects.all().order_by('-id').filter(is_active=False)
    return render(request, 'adm/bloked_user.html',{'users':users})


def order_list(request):
    order_prodects = OrderProdect.objects.all().order_by("-created_at")
    context = {
        'order_prodects': order_prodects,
    }
    return render(request,'adm/orderlist.html',context)


def order_ststus(request):
    order_id = request.POST['id']
    status = request.POST['status']
    if status == 'Cancelled':

        cancel_order = OrderProdect.objects.get(id=order_id)
        Prodect.objects.filter(id=cancel_order.prodect.id).update(stock=cancel_order.prodect.stock + cancel_order.quantity)
        OrderProdect.objects.filter.update(status="Cancelled")(id=order_id)

    elif status == 'Return':

        cancel_order = OrderProdect.objects.get(id=order_id)
        Prodect.objects.filter(id=cancel_order.prodect.id).update(stock=cancel_order.prodect.stock + cancel_order.quantity)
        OrderProdect.objects.filter(id=order_id).update(status="Return")

    else:
        OrderProdect.objects.filter(id=order_id).update(status=status)

    return JsonResponse({'success': True})


def order_history(request):
    order_historys = OrderProdect.objects.filter(Q(status='Deliverd') | Q(status='Cancelled') | Q(status='Return')).order_by('-created_at')
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

def report(request):
    if request.method == 'POST':
        prodects = Prodect.objects.all()
        users = custom.objects.all()
        date_from = request.POST['datefrom']
        date_to = datetime.datetime.strptime(request.POST['dateto'], "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_to = datetime.datetime.strftime(date_to, "%Y-%m-%d")        
        order_prodects=OrderProdect.objects.filter(updated_at__range=[date_from,date_to])

        context = {
            'order_prodects': order_prodects,
            'users':users,
            'prodects':prodects,
            }
        return render(request, 'adm/report.html',context)
    else:
        prodects = Prodect.objects.all()
        users = custom.objects.all()
        order_prodects = OrderProdect.objects.all().order_by("-created_at")

        context = {
            'order_prodects': order_prodects,
            'users':users,
            'prodects':prodects,
        }
        return render(request,'adm/report.html',context)
        
def brand_list(request):
    brands = Brand.objects.all()

    context = {
        'brands':brands,
    }
    return render(request,"adm/brand_list.html",context)

def add_brand(request):
    if request.method == 'POST':
        brand_name                = request.POST['brand_name']
        brand_discription         = request.POST['brand_discription']
        brand_img                 = request.FILES['brand_img']
        if Brand.objects.filter(brand_name=brand_name).exists():
            messages.info(request,'brandagory name is alredy taken!!!')
            return redirect('/brand_add')
        else:
            barnds = Brand(brand_name=brand_name, brand_discription=brand_discription, brand_img=brand_img)
            barnds.save()
            return redirect('add_brand')
    else:
        return render(request,'adm/add_brand.html')


def edit_brand(request,id):
    print(id)
    brand = Brand.objects.get(id=id)
    if request.method == 'POST':

        if request.FILES.get('brand_img'):
            brand.brand_img            = request.FILES['brand_img']

        brand.brand_name                = request.POST['brand_name']
        brand.brand_discription         = request.POST['brand_discription']

        if Brand.objects.exclude(id=id).filter(brand_name=brand.brand_name).exists():
            messages.info(request,'Brand name is alredy taken!!!')
            return render(request, 'adm/edit_brand.html',{'id':id})
        else:
            brand.save()
            return redirect('brand_list')
    else:
        context = {
            'brand':brand,
        }
        return render(request,'adm/edit_brand.html',context)


def brand_del(request, id):
    Brand.objects.filter(id=id).delete()
    return redirect('brand_list')
