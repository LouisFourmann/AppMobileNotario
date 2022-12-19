from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from planning.serializers import EventSerializer, GetEventSerializer
from . import models

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


@api_view(['POST'])
def AddEvent(request):
    serializer = EventSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not request.user.is_authenticated:
        return response_code(401, {"msg": "Invalid user"})
    notary = get_or_none(models.Notary, user=request.user)
    if not notary:
        return response_code(403, {"msg", "Forbidden. You are not a notary."})
    event = models.Event.objects.create(
        notary=notary, **serializer.validated_data)
    if not event:
        return response_code(500, {"msg": "Internal Server Error"})
    event_serializer = GetEventSerializer(instance=event)
    return response_code(200, event_serializer.data)
    
@api_view(['POST', 'DELETE'])
def UpdateEvent(request, event_id):
    if request.method == 'POST':
        event = get_or_none(models.Event, pk=event_id)
        notary = get_or_none(models.Notary, user=request.user)
        if (event == None or event.notary != notary):
            return response_code(404, {"msg": "Not Found"})
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.is_authenticated:
            return response_code(401, {"msg": "Invalid user"})
        event.name = serializer.data["name"]
        event.description = serializer.data["description"]
        event.begin = serializer.data["begin"]
        event.end = serializer.data["end"]
        event.event_type = serializer.data["event_type"]
        if "client" in serializer.data:
            event.client = serializer.data["client"]
        event.save()
        return response_code(200, serializer.data)
    elif request.method == 'DELETE':
        event = get_or_none(models.Event, pk=event_id)
        notary = get_or_none(models.Notary, user=request.user)
        if not notary:
            return response_code(403, {"msg", "Forbidden. You are not a notary."})
        if not event:
            return response_code(404, {"msg": "Not Found"})
        if event.notary != notary:
            return response_code(403, {"msg": "Forbidden. You are not the owner of this event."})
        event.delete()
        return response_code(200, {"msg": "Event deleted."})

@api_view(['GET'])
def GetEvents(request):
    norary = get_or_none(models.Notary, user=request.user)
    if not norary:
        return response_code(403, {"msg", "Forbidden. You are not a notary."})
    events = models.Event.objects.filter(notary=norary.pk).all()
    events = events.order_by("begin")
    serializer = GetEventSerializer(events, many=True)
    return Response(serializer.data, status=200)