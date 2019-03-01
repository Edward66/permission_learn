from django.shortcuts import HttpResponse, render, redirect, reverse

from rbac import models
from rbac.forms.menu import MenuModelForm
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
    context = {
        'menus': menus,
        'menu_id': menu_id,
        'second_menus': second_menus,
        'second_menu_id': second_menu_id,
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
