from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetQuestion, name='GetQuestion'),
]