from django.urls import path
from knox import views as knox_view

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', knox_view.LogoutView.as_view(), name='logout'),
]