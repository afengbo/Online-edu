#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/09/12 9:38'
import re

from django import forms

from apps.operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'telephone', 'course_name']

    def clean_telephone(self):
        '''验证手机号码是否合法'''
        telephone = self.cleaned_data['telephone']
        REGEX_PHONE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        phone = re.compile(REGEX_PHONE)
        if phone.match(telephone):
            return telephone
        else:
            raise forms.ValidationError('手机号码非法', code='phone_invalid')
