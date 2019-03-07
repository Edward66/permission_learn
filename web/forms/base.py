from django import forms


class BaseBootStrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseBootStrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
