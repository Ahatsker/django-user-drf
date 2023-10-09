from django import forms
from register.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=40)
    password = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput)
