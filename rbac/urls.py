from django.urls import path, re_path

from rbac.views import role
from rbac.views import user
from rbac.views import menu

urlpatterns = [
    # 角色管理
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/add/$', role.role_add, name='role_add'),
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),
    re_path(r'^role/delele/(?P<pk>\d+)/$', role.role_delele, name='role_delete'),

    # 用户管理
    re_path(r'^user/list/$', user.user_list, name='user_list'),
    re_path(r'^user/add/$', user.user_add, name='user_add'),
    re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    re_path(r'^user/delele/(?P<pk>\d+)/$', user.user_delele, name='user_delete'),
    re_path(r'^user/reset/password/(?P<pk>\d+)$', user.user_reset_pwd, name='user_reset_pwd'),

    # 权限分配的一级菜单
    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/delete/(?P<pk>\d+)/$', menu.menu_delete, name='menu_delete'),

    # 权限分配的二级菜单
    # 权限分配之一级菜单
    re_path(r'^second/menu/add/(?P<menu_id>\d+)$', menu.second_menu_add, name='second_menu_add'),
    re_path(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    re_path(r'^second/menu/delete/(?P<pk>\d+)/$', menu.second_menu_delete, name='second_menu_delete')
]
