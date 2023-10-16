from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from register.models import User
from django.http import HttpResponse
from django.conf import settings
import jwt
import datetime
from .forms import UserLoginForm
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


# jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]) # при login и при входе на сайт
# from django.views.decorators.http import require_POST

# Create your views here.
def login(request):
    session = request.session
    if request.method == "POST":
        new_user_login = request.POST.get('username')
        new_user_password = request.POST.get('password')

        if User.objects.filter(username=new_user_login,
                               password=hashlib.md5(str.encode(new_user_password)).hexdigest(),):
            session[settings.USER_SESSION_ID] = jwt.encode(
                {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=180),
                 'username': new_user_login
                 },
                settings.SECRET_KEY, algorithm="HS256")
            return HttpResponse("Успешный вход", status=200)
        else:
            return HttpResponse("Неверный логин или пароль", status=500)

    if request.method == "GET":
        if request.user.is_authenticated:
            user_form = UserLoginForm
            return render(request, 'login/login.html', {'user_form': user_form})
        else:
            user_form = UserLoginForm
            return render(request, 'login/login.html', {'user_form': user_form})




class LoginAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
        # try:
        #     jwt.decode(request.session[settings.USER_SESSION_ID], settings.SECRET_KEY, algorithms=["HS256"])
        # except:
        #     return Response({'Login error': 'Пожалуйста авторизуйтесь'})  # ответ в ввиде json
        #
        # return Response(
        #     {'Login success': User.objects.get(username=jwt.decode(request.session[settings.USER_SESSION_ID],
        #                                                            settings.SECRET_KEY, algorithms=["HS256"])[
        #         'username']).username})

    # def post(self, request, format=None):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         session = request.session
    #         username = str(request.data['username'])
    #         password = str(request.data['password'])
    #         print(username)
    #         if User.objects.filter(username=username, password=hashlib.md5(str.encode(password)).hexdigest(), ):
    #             session[settings.USER_SESSION_ID] = jwt.encode(
    #                 {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=180),
    #                  'username': username
    #                  },
    #                 settings.SECRET_KEY, algorithm="HS256")
    #             return HttpResponse("Успешный вход", status=status.HTTP_200_OK)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

