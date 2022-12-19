from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import BadRequest, PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.template.defaulttags import csrf_token
from django.middleware.csrf import CsrfViewMiddleware
from django.template.context_processors import csrf
from django.middleware.csrf import get_token
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions

from knox.views import LoginView as KnoxLoginView
from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.response import Response

def response_code(code: int, data: dict = None):
    if not data:
        data = []
    data['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

class LoginView(KnoxLoginView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if user is not None:
            user_serialiser = UserSerializer(user)
            login(request, user)
            data = super().post(request, format)
            data.data['user'] = user_serialiser.data
            return data
        else:
            return response_code(401, {"msg": "User dosn't exist"})

class RegisterView(KnoxLoginView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = authenticate(request, **serializer.validated_data)
        if user is not None:
            user_serialiser = UserSerializer(user)
            login(request, user)
            data = super().post(request, format)
            data.data['user'] = user_serialiser.data
            return data
        else:
            return response_code(500, {"msg": "Internal Server Error"})