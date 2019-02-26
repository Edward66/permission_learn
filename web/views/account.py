from django.shortcuts import redirect, render

from web.forms.accounts import LoginForm
from rbac import models  # 不太规范的，以后再改


def login(request):
    forms = LoginForm()

    if request.method == 'POST':
        forms = LoginForm(request.POST)
        errors = forms.errors.get('__all__')
        if forms.is_valid():
            # 获取当前用户
            user = request.POST.get('name')
            pwd = request.POST.get('password')
            current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()

            # 获取当前用户的所有权限
            # 一个人可以有多个角色，那这些角色之间可能会有相同的权限（url），所以要去重（distinct)。
            # 在创建角色的时候可能没有给角色分配权限，这样在角色权限关系表中就会有角色对应null，我们不需要这样的信息。
            # 所以要过滤掉filter(permissions__isnull=False)
            permission_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                              'permissions__url').distinct()

            # 获取权限中所有的URL
            permission_list = [item['permissions_url'] for item in permission_queryset]

            # 把用户权限放入session中
            request.session['permission_url_list_key'] = permission_list

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
