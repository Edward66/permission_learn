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
    menu_queryset = models.Menu.objects.all()

    menu_id = request.GET.get('mid')

    context = {
        'menu_list': menu_queryset,
        'menu_id': menu_id
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
