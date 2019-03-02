from django.shortcuts import HttpResponse, render, redirect

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm
from rbac.service.urls import memory_reverse


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
