from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.conf import settings
import jwt
import datetime
from rest_framework import generics
from .serializers import UserSerializer
import hashlib

# jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]) # при login и при входе на сайт
# from django.views.decorators.http import require_POST

# Create your views here.
def register(request):
    session = request.session
    if request.method == "POST":
        new_user = request.POST.get('username')
        if User.objects.filter(username=new_user):
            return HttpResponse("Такой пользователь уже существует", status=500)
        else:
            User.objects.create(username=request.POST.get('username'),
                                password=hashlib.md5(str.encode(request.POST.get('password'))).hexdigest(),
                                age=request.POST.get('age'),
                                gender=request.POST.get('gender')
                                )
            session[settings.USER_SESSION_ID] = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=30)},
                                                            settings.SECRET_KEY, algorithm="HS256")
            return HttpResponse("Успешная регистрация", status=200)

    if request.method == "GET":
        # print(jwt.decode(session[settings.USER_SESSION_ID], settings.SECRET_KEY, algorithms=["HS256"]))
        user_form = UserRegisterForm
        return render(request, 'register/register.html', {'user_form':user_form})


class RegisterAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

