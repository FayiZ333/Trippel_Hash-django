from os import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.hom,name='hom'),
    path('search',views.search,name='search'),
    path('products',views.products,name='products'),
    # path('<slug:cat_slug>/',views.cat_pro,name='cat_pro'),
    path('<slug:cat_slug>/<slug:slug>/',views.single,name='single'),
    # path('single',views.single,name='single'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('reg',views.reg,name='reg'),
    path('signupcheck',views.signupcheck,name='signupcheck'),
    path('forgot',views.forgot,name='forgot'),
    path('otp_log', views.otp_log,name='otp_log'),
    path('new_pass',views.new_pass,name='new_pass'),
    path('profile',views.profile,name='profile'),
    path('men',views.men,name='men'),
    path('women',views.women,name='women'),
    path('order_cancel/<orderPro_id>',views.order_cancel,name='order_cancel'),
    path('order_return/<orderPro_id>',views.order_return,name='order_return'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('address_delete/<address_id>',views.address_delete,name='address_delete'),
    path('address_edit/<address_id>',views.address_edit,name='address_edit'),
    path('change_pass/<user_id>',views.change_pass,name='change_pass'),

]