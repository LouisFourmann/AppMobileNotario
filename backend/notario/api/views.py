from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def custom(request):
    if request.user.is_authenticated:
    # Do something for authenticated users.
        print("the user is auth")
    else:
    # Do something for anonymous users.
        print("user not log")