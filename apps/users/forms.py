#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:${'Aaron'} 
@time: 2018/04/09 
"""
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=5)
    password = forms.CharField(required=True)