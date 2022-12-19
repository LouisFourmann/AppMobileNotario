from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetChats, name='GetChats'), # Get all messages
    path('<int:chat_id>', views.GetChat, name='GetChat'), # Get all chats
    path('add/', views.AddMessage, name='add'), # POST
]