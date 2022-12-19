from rest_framework import serializers
from .models import Event
from notario.settings import AUTH_USER_MODEL
from accounts.models import User

class EventSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    begin = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=False)
    event_type = serializers.ChoiceField(choices=Event.CHOICES, required=True)
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

class GetEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"