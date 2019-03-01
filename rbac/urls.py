from django.urls import path, re_path

from rbac.views import role


urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/add/$', role.role_add, name='role_add'),
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),
    re_path(r'^role/delele/(?P<pk>\d+)/$', role.role_delele, name='role_delete'),
]