from django import forms

from rbac.models import UserInfo

from .base import BaseBootStrapForm


class LoginForm(BaseBootStrapForm):
    class Meta:
        model = UserInfo

        fields = ('name', 'password',)

        label = {
            'name': '用户名',
            'password': '密码',
        }

    def clean(self):
        input_username = self.cleaned_data.get('name')
        input_password = self.cleaned_data.get('password')

        if input_username and input_password:
            user_obj = UserInfo.objects.filter(name=input_username, password=input_password).first()
            print(user_obj)
            if not user_obj:
                raise forms.ValidationError('用户名或密码错误')
            else:
                return self.cleaned_data
