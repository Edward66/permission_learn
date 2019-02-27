from django.shortcuts import redirect, render

from web.forms.accounts import LoginForm
from rbac import models  # 不太规范的，以后再改
from rbac.service.init_permission import init_permission


def login(request):
    forms = LoginForm()

    # 1. 用户登陆
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        errors = forms.errors.get('__all__')
        if forms.is_valid():
            # 获取当前用户
            user = request.POST.get('name')
            pwd = request.POST.get('password')
            current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()

            # 2.权限信息初始化
            init_permission(current_user, request)

            return redirect('/customer/list/')

        context = {
            'forms': forms,
            'errors': errors
        }
        return render(request, 'login.html', context=context)

    context = {
        'forms': forms
    }
    return render(request, 'login.html', context=context)
