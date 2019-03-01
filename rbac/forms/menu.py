from django import forms

from rbac import models


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MenuModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
