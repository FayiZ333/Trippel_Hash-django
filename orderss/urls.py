from django.urls import path
from . import views

urlpatterns = [

    path('place_order',views.place_order,name='place_order'),
    path('pay',views.pay,name='pay'),
    path('success/<ord_no>',views.success,name='success'),
    path('buynow_place_order', views.buynow_place_order, name='buynow_place_order'),
    path('buynow_payments', views.buynow_payments, name='buynow_payments'),
    




    
]