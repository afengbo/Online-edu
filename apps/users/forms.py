#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/08/17 16:47'
from django import forms
from captcha.fields import CaptchaField

from apps.users.models import UserProfile


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, max_length=16)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=16)
    password2 = forms.CharField(required=True, min_length=6, max_length=16)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'telphone']
