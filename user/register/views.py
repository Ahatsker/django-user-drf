from django.forms import model_to_dict
from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView

from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.conf import settings
import jwt
import datetime
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
import hashlib
from rest_framework import status


# jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]) # при login и при входе на сайт
# from django.views.decorators.http import require_POST

# Create your views here.
# def register(request):
#     session = request.session
#     if request.method == "POST":
#         new_user = request.POST.get('username')
#         if User.objects.filter(username=new_user):
#             return HttpResponse("Такой пользователь уже существует", status=500)
#         else:
#             User.objects.create(username=new_user,
#                                 password=hashlib.md5(str.encode(request.POST.get('password'))).hexdigest(),
#                                 age=request.POST.get('age'),
#                                 gender=request.POST.get('gender')
#                                 )
#             session[settings.USER_SESSION_ID] = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=30),
#                                                             'username': new_user},
#                                                             settings.SECRET_KEY, algorithm="HS256")
#             return HttpResponse("Успешная регистрация", status=200)
#
#     if request.method == "GET":
#         # print(jwt.decode(session[settings.USER_SESSION_ID], settings.SECRET_KEY, algorithms=["HS256"]))
#         user_form = UserRegisterForm
#         return render(request, 'register/register.html', {'user_form':user_form})


class ChangeAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        User.objects.create_user(username=request.data['username'],
                                 password=request.data['password'])
        return Response({'post': 'Done'}, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         session = request.session
    #         new_username = request.data['username']
    #
    #         if User.objects.filter(username=new_username):
    #             return Response({'post': 'Пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             new_user = User.objects.create(username=new_username,
    #                                            password=hashlib.md5(str.encode(request.data['password'])).hexdigest(),
    #                                            age=request.data['age'],
    #                                            gender=request.data['gender']
    #                                            )
    #             session[settings.USER_SESSION_ID] = jwt.encode(
    #                 {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=30),
    #                  'username': new_username},
    #                 settings.SECRET_KEY, algorithm="HS256")
    #         return Response({'post': 'Done'}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request):
    #     username = request.data['username']
    #
    #     if username == jwt.decode(request.session[settings.USER_SESSION_ID],settings.SECRET_KEY, algorithms=["HS256"])['username']:
    #         User.objects.update(username=username,
    #                            password=request.data['password'],
    #                            age=request.data['age'],
    #                            gender=request.data['gender']
    #                            )
    #         return Response({'update': 'Done'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'update': 'Done'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # def delete(self, request):
    #     username = request.data['username']
    #     if username == jwt.decode(request.session[settings.USER_SESSION_ID],settings.SECRET_KEY, algorithms=["HS256"])['username']:
    #         del_user = User.objects.get(username=username)
    #         del_user.delete()
    #         return Response({'update': 'Done'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'update': 'Done'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
