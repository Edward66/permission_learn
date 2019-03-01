from django import forms

from rbac import models


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        检测两次密码是否一致
        :return:
        """
        passwrod = self.cleaned_data.get('password')
        confirm_paassword = self.cleaned_data.get('confirm_password')

        if passwrod and confirm_paassword:
            if passwrod != confirm_paassword:
                raise forms.ValidationError('两次密码输入不一致')
            else:
                return confirm_paassword


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResetPwdUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(ResetPwdUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        检测两次密码是否一致
        :return:
        """
        passwrod = self.cleaned_data.get('password')
        confirm_paassword = self.cleaned_data.get('confirm_password')

        if passwrod and confirm_paassword:
            if passwrod != confirm_paassword:
                raise forms.ValidationError('两次密码输入不一致')
            else:
                return confirm_paassword
