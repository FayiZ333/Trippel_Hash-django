from django.db.models.expressions import F, Exists
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from carts.models import Cart, Cart_item
from panel.models import custom, Prodect, Catagory
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from orderss.models import OrderProdect


# Create your views here.

# @login_required(login_url='login')
def hom(request):
    prodects = Prodect.objects.all()

    context= {
        'prodects' : prodects,
    }
    return render(request, 'userst/index.html',context)


def men(request):
    prodects = Prodect.objects.filter(gender = 'Men')
    context= {
        'prodects' : prodects
    }
    return render(request, 'userst/men.html',context)

def women(request):
    prodects = Prodect.objects.filter(gender = 'Women')
    context= {
        'prodects' : prodects
    }
    return render(request, 'userst/women.html',context)

def products(request):
    prodects = Prodect.objects.all().order_by('-date')

    context= {
        'prodects' : prodects
    }
    return render(request, 'userst/products.html',context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        users =  auth.authenticate(email=email, password=password)

        if users is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = Cart_item.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = Cart_item.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = users
                        item.save()
            except:
                pass
            auth.login(request,users)
            return redirect('hom')
        else:
            messages.error(request,'Invalid Input!!!')
            return redirect('login')
    else:  
        return render(request, 'login/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def forgot(request):
    if request.method == "POST":
        phone       = request.POST['phone']

        if custom.objects.filter(phone=phone).exists():
            request.session['phone_number'] = phone

            account_sid = 'AC44b0c6232c417049d89e3529e316e6e6'
            auth_token = 'cab685a91908567662aa334047df8a0a'
            client = Client(account_sid, auth_token)

            verification = client.verify \
                                .services('VA349a204423937620d2dedcd5372aa431') \
                                .verifications \
                                .create(to='+91' +phone, channel='sms')

            print(verification.status)
            
            return redirect('otp_log')
        else:
            messages.error(request,'Phone number not registerd!!!')
            return redirect('forgot') 
           

    return render(request,'login/forgotton.html')



def otp_log(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        second = request.POST.get('second')
        third = request.POST.get('third')
        fourth = request.POST.get('fourth')
        fifth = request.POST.get('fifth')
        sixth = request.POST.get('sixth')


        otp = first+second+third+fourth+fifth+sixth

        phone = request.session['phone_number']
        request.session['phone_number'] = phone

        account_sid = 'AC44b0c6232c417049d89e3529e316e6e6'
        auth_token = 'cab685a91908567662aa334047df8a0a'
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                                .services('VA349a204423937620d2dedcd5372aa431') \
                                .verification_checks \
                                .create(to='+91' +phone, code=otp)

        print(verification_check.status)
        if verification_check.status == 'approved':
            return redirect('new_pass')
        else:
            messages.error(request,'OTP is not currect!!!')
            return redirect('otp_log')
                
    else:
        return render(request, 'login/otp_login.html')


def new_pass(request):
    if request.method == 'POST':
        password          = request.POST['password']
        password2         = request.POST['password2']

        print(password)
        print(password2)

        if password == password2:
            phone = request.session['phone_number']
            user = custom.objects.get(phone=phone)
            user.set_password(password)
            user.save()
            return redirect('login')

        else:
            messages.error(request,'Pssword is not matching!!!')
            return redirect('new_pass')


    else:
        return render(request,'login/new_password.html')





def reg(request):
    
    if request.method == "POST":
        # firstname = request.POST['firstname']
        # lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']

        # for otp #
        ############

        request.session['email'] = email
        request.session['phone_number'] = phone
        request.session['password'] = pass1
        request.session['username'] = username


        if pass1 == pass2:
            if custom.objects.filter(username=username).exists():
                messages.info(request,'user name is alredy taken!!!')
                return redirect('/reg')
            elif custom.objects.filter(email=email).exists():
                messages.info(request,'email id is alredy taken!!!')
                return redirect('/reg')
            elif custom.objects.filter(phone=phone).exists():
                messages.error(request,'Phone number is alredy taken!!!')
                return redirect('/reg')

            else:
                # users = custom.objects.create_user(username=username, phone=phone, password=pass1, email=email)
                # users.save()
                # return redirect('hom')
                account_sid = 'AC44b0c6232c417049d89e3529e316e6e6'
                auth_token = 'cab685a91908567662aa334047df8a0a'
                client = Client(account_sid, auth_token)

                verification = client.verify \
                                    .services('VA349a204423937620d2dedcd5372aa431') \
                                    .verifications \
                                    .create(to='+91' +phone, channel='sms')

                print(verification.status)


                return render(request, 'login/otp_reg.html')
        else:            
            messages.info(request,'Pssword is not maching!!!')
            return redirect('reg')
    else:
        return render(request, 'login/register.html')


def signupcheck(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        second = request.POST.get('second')
        third = request.POST.get('third')
        fourth = request.POST.get('fourth')
        fifth = request.POST.get('fifth')
        sixth = request.POST.get('sixth')


        otp = first+second+third+fourth+fifth+sixth

        email = request.session['email']
        phone = request.session['phone_number']
        pass1 = request.session['password']
        username =request.session['username'] 



        account_sid = 'AC44b0c6232c417049d89e3529e316e6e6'
        auth_token = 'cab685a91908567662aa334047df8a0a'
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                                .services('VA349a204423937620d2dedcd5372aa431') \
                                .verification_checks \
                                .create(to='+91' +phone, code=otp)

        print(verification_check.status)
        if verification_check.status == 'approved':
            user = custom.objects.create_user(email=email,password=pass1,username=username,phone=phone)
            user.save()
            auth.login(request, user)
            return redirect('hom')
        else:
            messages.error(request,'OTP is not currect!!!')
            return redirect('signupcheck')
                
        print('working')
        del request.session['email']
        del request.session['phone']
        del request.session['username'] 
        del request.session['password']
    else:
        return render(request, 'login/otp_reg.html')

def cat_pro(request,cat_slug=None):

    catagories = None
    prodects = None


    if cat_slug != None:
        catagories      = get_object_or_404(cat_slug)
        prodects = Prodect.objects.filter(catagory=catagories)
        prodect_count = prodects.count()
    else:
        prodects = Prodect.objects.all().order_by(id)
        prodect_count = prodects.count()

    context = {
        "prodects" : prodects,
        "prodect_count" : prodect_count,
    }
    return render(request, 'userst/cat.html',context)


def single(request,cat_slug,slug):
    try:
        single_pro = Prodect.objects.get(catagory__cat_slug=cat_slug, slug=slug)
    except Exception as e:
        raise e
    prodects = Prodect.objects.all()

    context = {
        'single_pro' : single_pro,                                              
        'prodects':prodects
    }
    return render(request,'userst/single.html', context)


def profile(request):

    order_prodects = OrderProdect.objects.filter(user_id=request.user.id).order_by('-id')
    context = {
        'order_prodects':order_prodects,
    }
    return render(request,'userst/profile.html',context)

def order_cancel(request,orderPro_id):
    
    cancel_order = OrderProdect.objects.get(id=orderPro_id)
    Prodect.objects.filter(id=cancel_order.prodect.id).update(stock=cancel_order.prodect.stock + cancel_order.quantity)
    OrderProdect.objects.filter(id=orderPro_id).update(status="Cancelled")
    return redirect('profile')

def order_return(request,orderPro_id):

    cancel_order = OrderProdect.objects.get(id=orderPro_id)
    Prodect.objects.filter(id=cancel_order.prodect.id).update(stock=cancel_order.prodect.stock + cancel_order.quantity)

    OrderProdect.objects.filter(id=orderPro_id).update(status="Return")
    return redirect('profile')


def edit_profile(request):
    users = custom.objects.get(id=request.user.id)
    
    if request.method == 'POST':

        email           = request.POST.get('email')
        username     = request.POST.get('username')
        phone        = request.POST.get('phone')
        gender          = request.POST.get('gender')
        country           = request.POST.get('country')
        state           = request.POST.get('state')
        address     = request.POST.get('address')
        district           = request.POST.get('district')

        # profile_img      = request.FILES.get('profile_img')


        if custom.objects.exclude(id=request.user.id).filter(username=users.username).exists():
            messages.error(request,'user name is already taken!')
            return render(request,'userst/profile.html',{'id':request.user.id})

        elif custom.objects.exclude(id=request.user.id).filter(email=users.email).exists():
            messages.error(request,'email is already taken!')
            return render(request,'userst/profile.html',{'id':request.user.id})

        else:
            users = custom.objects.filter(id=request.user.id).update(email=email, username=username, phone=phone, gender=gender,
            country=country,state=state,address=address, district=district)
            return redirect('profile')

    else:
        context = {'users':users}
        return render(request,'userst/profile.html',context) 




##############################################



def test(request):
    return render(request,'userst/test.html')



##############################################
