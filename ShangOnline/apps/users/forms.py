from django import forms
from captcha.fields import CaptchaField
from .models import UsersProFile,EmailVerify
import re


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '邮箱最大位数为30',
        'min_length': '邮箱最小位数为5',
        'required': '邮箱不能为空'
    })

    password = forms.CharField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '密码最大位数为30',
        'min_length': '密码最小位数为5',
        'required': '密码不能为空'
    })

    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '邮箱最大位数为30',
        'min_length': '邮箱最小位数为5',
        'required': '邮箱不能为空'
    })

    password = forms.CharField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '密码最大位数为30',
        'min_length': '密码最小位数为5',
        'required': '密码不能为空'
    })


class ForgetForm(forms.Form):
    email = forms.EmailField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '邮箱最大位数为30',
        'min_length': '邮箱最小位数为5',
        'required': '邮箱不能为空'
    })
    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })


class ResetForm(forms.Form):
    defemail = forms.EmailField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '邮箱最大位数为30',
        'min_length': '邮箱最小位数为5',
        'required': '邮箱不能为空'
    })

    password = forms.CharField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '密码最大位数为30',
        'min_length': '密码最小位数为5',
        'required': '密码不能为空'
    })

    password1 = forms.CharField(max_length=30, min_length=5, required=True, error_messages={
        'max_length': '密码最大位数为30',
        'min_length': '密码最小位数为5',
        'required': '密码不能为空'
    })

    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })


class UserImageChangeForm(forms.ModelForm):
    class Meta:
        model = UsersProFile()
        fields = ['image']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UsersProFile()
        fields = ['nike_name', 'birthday', 'gender', 'address', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        check = re.compile('^(13\d|14[57]|15\d|166|17[367]|18\d)\d{8}$')

        pho = check.match(phone)
        if pho:
            return phone
        else:
            raise forms.ValidationError('手机验证不合法')


class UserSendCodeForm(forms.ModelForm):
    class Meta:
        model = UsersProFile
        fields = ['email']


class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerify
        fields = ['email','code']
