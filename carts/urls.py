from django.urls import path
from . import views


urlpatterns = [

    path('',views.cart, name='cart'),
    path('add_cart/<int:id>',views.add_cart, name="add_cart"),
    path('remove_cart_item/<int:id>',views.remove_cart_item, name='remove_cart_item'),
    path('remove_cart/<int:id>',views.remove_cart, name="remove_cart"),
    path('remove_cart_item', views.remove_cart_item, name='remove_cart_item'),
    path('check_out',views.check_out,name='check_out'),
    # path('payments',views.payments,name='payments'),
    

]