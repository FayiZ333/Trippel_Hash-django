from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse

from panel.models import Prodect
from .models import Wish_list

# Create your views here.

def add_wish(request,id):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    prodect = Prodect.objects.get(id=id)
    if Wish_list.objects.filter(prodect=prodect,user=user).exists():
        pass
    else:
        wish = Wish_list.objects.create(prodect=prodect,user=user)
    return redirect(url)

def rm_wish(request,id):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    prodect = Prodect.objects.get(id=id)
    wish = Wish_list.objects.filter(prodect=prodect,user=user).delete()
    return redirect(url)

def wish_list(request):
    wishes = Wish_list.objects.filter(user=request.user)
    context = {
        'wishes':wishes,
    }
    return render(request,'userst/wish_list.html',context)


