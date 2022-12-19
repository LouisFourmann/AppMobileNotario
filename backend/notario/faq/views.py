from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import models, serializers
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def GetQuestion(request):
    questions = models.Question.objects.all()
    serializer = serializers.GetQuestionSerializer(questions, many=True)
    return Response(serializer.data, status=200)
