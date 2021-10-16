from django.urls import path
from . import views

urlpatterns = [

    path('place_order',views.place_order,name='place_order'),
    path('pay',views.pay,name='pay'),
    path('success/<ord_no>',views.success,name='success'),



    
]