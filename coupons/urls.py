from django.urls import path
from . import views

urlpatterns = [

path('checkCoupon', views.checkCoupon, name="checkCoupon"),
path('admin_coupon', views.admin_coupon, name="admin_coupon"),
path('admin_coupon_list', views.admin_coupon_list, name="admin_coupon_list"),
path('coupon_edit/<id>', views.coupon_edit, name="coupon_edit"),
path('coupon_delete', views.coupon_delete, name="coupon_delete"),



]