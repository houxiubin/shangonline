from django import forms
from .models import UserAskInfo
import re

class UserAskInfoForm(forms.ModelForm):
    class Meta():
        model=UserAskInfo
        # fields='__all__'
        fields=['name','phone','course']
        # exclude=['add_time']

    def clean_phone(self):
        phone=self.cleaned_data['phone']

        pho=re.compile(r'^(13\d|14[57]|15\d|166|17[367]|18\d)\d{8}$')
        if pho.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号格式不正确')


class UserCommentForm(forms.Form):
    content=forms.CharField(min_length=5,max_length=200,required=True)
    courseid=forms.IntegerField(required=True)