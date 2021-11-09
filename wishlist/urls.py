from django.urls import path
from . import views

urlpatterns = [
    path('add_wish/<id>',views.add_wish,name='add_wish'),
    path('rm_wish/<id>',views.rm_wish,name='rm_wish'),
    path('wish_list',views.wish_list,name='wish_list'),


]