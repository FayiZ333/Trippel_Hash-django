from django.urls import path
from . import views

urlpatterns = [

    path('',views.adhom,name='adhom'),
    path('prolist',views.prolist,name='prolist'),
    path('proadd',views.proadd,name='proadd'),
    path('delete',views.delete,name='delete'),
    # path('update/<id>', views.update,name='update'),
    path('edit/<id>', views.edit,name='edit'),
    path('cat_add',views.cat_add,name='cat_add'),
    path('cat_list',views.cat_list,name='cat_list'),
    path('cat_delete',views.cat_delete,name='cat_delete'),
    path('user_list',views.user_list,name='user_list'),
    path('block',views.block,name='block'),
    path('unblock',views.unblock,name='unblock'),
    path('blocked_users',views.blocked_users,name='blocked_users'),
    path('order_list',views.order_list,name='order_list'),
    path('order_ststus/<order_id>',views.order_ststus,name='order_ststus'),
    path('order_history',views.order_history,name='order_history'),
    path('submit_review/<prodect_id>',views.submit_review,name='submit_review'),
    path('report',views.report,name='report'),

    




]