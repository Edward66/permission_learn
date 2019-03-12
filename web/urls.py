from django.conf.urls import re_path, include
from web.views import customer
from web.views import payment
from web.views import accounts

urlpatterns = [

    re_path(r'^customer/list/$', customer.customer_list, name='customer_list'),
    re_path(r'^customer/add/$', customer.customer_add, name='customer_add'),
    re_path(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name='customer_edit'),
    re_path(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name='customer_del'),
    re_path(r'^customer/import/$', customer.customer_import, name='customer_import'),
    re_path(r'^customer/tpl/$', customer.customer_tpl, name='customer_tpl'),

    re_path(r'^payment/list/$', payment.payment_list, name='payment_list'),
    re_path(r'^payment/add/$', payment.payment_add, name='payment_add'),
    re_path(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit, name='payment_edit'),
    re_path(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del, name='payment_del'),

    # 登陆
    re_path(r'login/$', accounts.login, name='login'),

]
