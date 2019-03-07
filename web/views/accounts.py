from django.shortcuts import render, redirect

from web.forms.accounts import LoginForm
from rbac import models
from rbac.service.init_permission import init_permission


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

        init_permission(current_user, request)

        return redirect('/customer/list/')

    context = {
        'forms': forms,
        'errors': errors
    }
    return render(request, 'login.html', context)
