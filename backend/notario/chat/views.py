from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models, serializers
from accounts.models import User

def response_code(code: int, data: dict = None):
    if not data:
        data = []
    data['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.MultipleObjectsReturned as e:
        print(e)
        return None
    except classmodel.DoesNotExist as e:
        print(e)
        return None

@api_view(['GET'])
def GetChat(request, chat_id):
    chat = get_or_none(models.Chat, pk=chat_id)
    if not chat:
        return response_code(404, {"msg": "Chat not found"})
    messages =  models.Message.objects.filter(chat=chat.pk).all()
    messages = messages.order_by("created_at")
    serializer = serializers.GetMessage(messages, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def GetChats(request):
    user = request.user
    chats = models.Chat.objects.filter(user_one=user).all()
    chats = chats.union(models.Chat.objects.filter(user_two=user).all())
    serializer = serializers.GetChat(chats, many=True)
    data = []
    for chat in serializer.data:
        receiver_id = chat['user_one']
        if chat['user_one'] == user.pk:
            receiver_id = chat['user_two']
        receiver: User = get_or_none(models.User, pk=receiver_id)
        name = f"{receiver.first_name} {receiver.last_name}"
        data.append({
            "id": chat['id'],
            "user_name": name,
            "user_id": receiver.pk,
        })
    return Response(data, status=200)

@api_view(['POST'])
def AddMessage(request):
    serializer = serializers.AddMessage(data=request.data)
    serializer.is_valid(raise_exception=True)
    receiver_id = serializer.data["receiver"]
    receiver = get_or_none(models.User, pk=receiver_id)
    if not receiver:
        return response_code(404, {"msg": "User id not found"})
    sender = request.user
    chat = get_or_none(models.Chat, user_one=sender, user_two=receiver)
    if not chat:
        chat = get_or_none(models.Chat, user_one=receiver, user_two=sender)
    if not chat:
        chat = models.Chat.objects.create(
            user_one=sender,
            user_two=receiver
        )
    models.Message.objects.create(
        sender=sender,
        receiver=receiver,
        chat=chat,
        text=serializer.data['text']
    )
    return response_code(200, {"msg": "Message send"})

