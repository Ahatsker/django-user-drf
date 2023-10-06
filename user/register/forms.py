from django import forms
from .models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=40)
    password = forms.CharField(required=True, max_length=30)
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True, max_length=30)
