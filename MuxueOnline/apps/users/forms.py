# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 下午10:54
# @Author  : alvin
# @Email   : ylq.win@aliyun.com
# @File    : forms.py

from django import forms

class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)

