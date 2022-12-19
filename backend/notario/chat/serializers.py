from rest_framework import serializers
from .models import Chat, Message, User

class GetMessage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class AddMessage(serializers.Serializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    text = serializers.CharField(required=True)

class GetChat(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"