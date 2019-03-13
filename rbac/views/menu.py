from collections import OrderedDict

from django.forms import formset_factory
from django.shortcuts import HttpResponse, render, redirect, reverse

from rbac import models
from rbac.forms.menu import (
    MenuModelForm, SecondMenuModelForm, PermissionModelForm,
    MultiAddPermissionForm, MultiEditPermissionForm
)
from rbac.service.urls import memory_reverse
from rbac.service.router import get_all_url_dict


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menu_queryset = models.Menu.objects.all()

    menu_id = request.GET.get('mid')  # 用户选择的一级菜单

    menus_exists = models.Menu.objects.filter(id=menu_id).exists()

    if not menus_exists:
        menu_id = None

    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    second_menus_exists = models.Permission.objects.filter(id=second_menu_id).exists()

    if not second_menus_exists:
        second_menu_id = None

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid__id=second_menu_id)
    else:
        permissions = []

    context = {
        'menu_list': menu_queryset,
        'menu_id': menu_id,
        'second_menus': second_menus,
        'second_menu_id': second_menu_id,
        'permissions': permissions
    }

    return render(request, 'rbac/menu_list.html', context)


def menu_add(request):
    """
     菜单和权限列表
    :param request:
    :return:
    """
    if request.method == 'GET':
        forms = MenuModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = MenuModelForm(data=request.POST)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'forms': forms})


def menu_edit(request, pk):
    """
    编辑一级菜单
    :param request:
    :param pk:
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=pk).first()

    if not menu_obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        forms = MenuModelForm(instance=menu_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = MenuModelForm(data=request.POST, instance=menu_obj)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def menu_del(request, pk):
    """
    删除一级菜单
    :param request:
    :param pk:
    :return:
    """
    menu_list_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': menu_list_url})

    models.Menu.objects.filter(id=pk).delete()

    return redirect(menu_list_url)


# 二级菜单的增删改


def second_menu_add(request, menu_id):
    """
    增加二级菜单
    :param request:
    :param pk:  已经选择的一级菜单ID（用于设置默认值)
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        forms = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = SecondMenuModelForm(data=request.POST)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param pk:
    :return:
    """

    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        forms = SecondMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = SecondMenuModelForm(data=request.POST, instance=permission_obj)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'forms': forms})


def second_menu_del(request, pk):
    """
    删除二级菜单
    :param request:
    :param pk:
    :return:
    """

    menu_list_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': menu_list_url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(menu_list_url)


# 权限的增删改

def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param pk:
    :return:
    """

    if request.method == 'GET':
        forms = PermissionModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = PermissionModelForm(data=request.POST)
    if forms.is_valid():
        second_menu_obj = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_obj:
            return HttpResponse('二级菜单不存在,请重新选择')
        forms.instance.pid = second_menu_obj  # form.instance中包含用户提交的所有值
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def permission_edit(request, pk):
    """
    权限编辑
    :param request:
    :param pk: 要编辑的权限id
    :return:
    """
    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        forms = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = PermissionModelForm(data=request.POST, instance=permission_obj)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def permission_del(request, pk):
    """
    权限删除
    :param request:
    :param pk:
    :return:
    """
    menu_list_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': menu_list_url})

    models.Permission.objects.filter(id=pk).delete()

    return redirect(menu_list_url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    # 1. 获取项目中所有的url

    all_url_dict = get_all_url_dict()

    router_name_set = set(all_url_dict.keys())  # 所有路由中的url集合
    """
    set里不能有重复的值，转换成set后只会剩下key
     {
     'rbac:menu_list': {'name': 'rbac:menu_list', 'url': 'xxxxx/yyyy/menu/list'}
     } 
     会变成 {'rbac:menu_list'}
    """
    #

    # 2. 获取数据库中所有的url
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_name_set = set()  # 数据库中的set集合
    permission_dict = OrderedDict()

    for permission in permissions:
        permission_dict[permission['name']] = permission
        permission_name_set.add(permission['name'])

        """
           {
               'rbac:menu_list':{'id':1,'title':'角色列表',name:'rbac:role_list',url:'/rbac/role/list'},
               ......
           }
        """

    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name':'rbac:role_list','url':'/rbac/role/list'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中的不一致'

    # 3. 应该添加、删除和修改的权限

    # 3.1 计算出应该添加的name
    add_name_list = router_name_set - permission_name_set  # 所有路由中的url集合减去数据库中的url      集合

    add_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    generate_formset = add_formset_class(
        initial=[row_dict for name, row_dict in all_url_dict.items() if name in add_name_list]
    )

    # 3.2 计算出应该删除的name
    delete_name_list = permission_name_set - router_name_set  # 数据库里的url - 路由中的url = 数据库里有，路由中没有
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name
    update_name_list = permission_name_set & router_name_set  # 都包含的元素
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)
    update_formset = update_formset_class(
        initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list]
    )

    context = {
        'generate_formset': generate_formset,
        'delete_row_list': delete_row_list,
        'update_formset': update_formset,
    }

    return render(request, 'rbac/multi_permissions.html', context)
