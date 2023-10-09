from django.shortcuts import render, redirect
from register.models import User
from django.http import HttpResponse
from django.conf import settings
import jwt
import datetime
from .forms import UserLoginForm
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response

# jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]) # при login и при входе на сайт
# from django.views.decorators.http import require_POST

# Create your views here.
def login(request):
    session = request.session
    if request.method == "POST":
        new_user_login = request.POST.get('username')
        new_user_password = request.POST.get('password')

        if User.objects.filter(username=new_user_login,
                               password=hashlib.md5(str.encode(new_user_password)).hexdigest(), ):
            session[settings.USER_SESSION_ID] = jwt.encode(
                {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=180),
                 'username': new_user_login
                 },
                settings.SECRET_KEY, algorithm="HS256")
            return HttpResponse("Успешный вход", status=200)
        else:
            return HttpResponse("Неверный логин или пароль", status=500)

    if request.method == "GET":
        try:
            jwt.decode(session[settings.USER_SESSION_ID], settings.SECRET_KEY, algorithms=["HS256"])
        except:
            user_form = UserLoginForm
            return render(request, 'login/login.html', {'user_form': user_form})

        user_form = UserLoginForm
        return render(request, 'login/login.html', {'user_form': user_form})



class LoginAPIView(APIView):
    def get(self, request):
        try:
            jwt.decode(request.session[settings.USER_SESSION_ID], settings.SECRET_KEY, algorithms=["HS256"])
        except:
            return Response({'Login error': 'Пожалуйста авторизуйтесь'})  # ответ в ввиде json

        return Response({'Login success': User.objects.get(username=jwt.decode(request.session[settings.USER_SESSION_ID],
                                             settings.SECRET_KEY, algorithms=["HS256"])['username']).username})

    def post(self, request):
        return Response({'Register': 'Post'})