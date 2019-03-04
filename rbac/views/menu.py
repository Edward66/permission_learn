from collections import OrderedDict

from django.shortcuts import HttpResponse, render, redirect
from django.forms import formset_factory

from rbac import models
from rbac.forms.menu import (
    MenuModelForm, SecondMenuModelForm, PermissionModelForm,
    MultiAddPermissionForm, MultiEditPermissionForm
)
from rbac.service.urls import memory_reverse
from rbac.service.routers import get_all_url_dict


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menus_exists = models.Menu.objects.filter(id=menu_id).exists()
    if not menus_exists:
        menu_id = None

    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid__id=second_menu_id)
    else:
        permissions = []

    second_menus_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menus_exists:
        second_menu_id = None

    context = {
        'menus': menus,
        'menu_id': menu_id,
        'second_menus': second_menus,
        'second_menu_id': second_menu_id,
        'permissions': permissions,
    }
    return render(request, 'rbac/menu_list.html', context)


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()

        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def menu_delete(request, pk):
    """
    删除一级菜单
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Menu.objects.filter(id=pk).delete()

    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已经选择的一级菜单ID（用于设置默认值）
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param menu_id:
    :return:
    """
    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_delete(request, pk):
    """
    删除二级菜单
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()

    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu_obj = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_obj:
            return HttpResponse('二级菜单不存在，请重新选择!')
        # form.instance中包含用户提交的所有值
        form.instance.pid = second_menu_obj
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk: 要编辑的权限id
    :return:
    """
    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def permission_delete(request, pk):
    """
    删除权限
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    # 1.获取项目中所有的url

    """
         {
             'rbac:menu_list':{name:'rbac:role_list',url:'/rbac/role/list'},
             ......
         }
    """

    all_url_dict = get_all_url_dict()

    router_name_set = set(all_url_dict.keys())

    # 2.获取数据库中所有的url
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_name_set = set()
    permission_dict = OrderedDict()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])

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
            value['url'] = '路由和数据库中不一致'

    # 3. 应该添加、删除、修改的权限有哪些？
    # 3.1 计算出应该增加的name

    add_name_list = router_name_set - permission_name_set
    add_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    generate_formset = add_formset_class(
        initial=[row_dict for name, row_dict in all_url_dict.items() if name in add_name_list])

    # 3.2 计算出应该删除的name

    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name

    update_name_list = permission_name_set & router_name_set
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)
    update_formset = update_formset_class(
        initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    context = {
        'generate_formset': generate_formset,
        'delete_row_list': delete_row_list,
        'update_formset': update_formset,
    }
    return render(request, 'rbac/multi_permissions.html', context)
