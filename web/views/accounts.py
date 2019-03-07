from django.shortcuts import render, redirect

from web.forms.accounts import LoginForm
from rbac import models


def login(request):
    if request.method == 'GET':
        forms = LoginForm()
        return render(request, 'login.html', {'forms': forms})

    forms = LoginForm(data=request.POST)
    errors = forms.errors.get('__all__')
    if forms.is_valid():
        username = request.POST.get('name')
        password = request.POST.get('password')
        current_user = models.UserInfo.objects.filter(name=username, password=password).first()

        permission_queryset = current_user.roles.filter(permissions__isnull=False).values(
            'permissions__id',
            'permissions__url'
        ).distinct()

        permission_list = [item['permissions__url'] for item in permission_queryset]

        request.session['permission_url_list_key'] = permission_list

        return redirect('/customer/list/')

    context = {
        'forms': forms,
        'errors': errors
    }
    return render(request, 'login.html', context)
