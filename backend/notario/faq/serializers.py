from rest_framework import serializers
from .models import Question

class GetQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"