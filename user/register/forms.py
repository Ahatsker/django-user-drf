from django import forms
from .models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=40)
    password = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput)
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True, max_length=30)
