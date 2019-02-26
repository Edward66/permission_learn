from django import forms
from rbac.models import UserInfo  # 不太规范的，以后再改


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserInfo

        fields = ('name', 'password')

        label = {
            '用户名': 'name',
            '密码': 'password',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'name': {
                'max_length=': '不能超过32个字符',
                "required": "用户名不能为空",
            },
            'password': {
                'max_length': "不能超过64字符",
                "required": "密码不能为空",
            }
        }

    def clean(self):
        login_input_name = self.cleaned_data.get('name')
        login_input_pwd = self.cleaned_data.get('password')

        if login_input_name and login_input_pwd:
            user = UserInfo.objects.filter(name=login_input_name, password=login_input_pwd).first()
            if user:
                return self.cleaned_data
            else:
                raise forms.ValidationError('用户名或密码错误')
