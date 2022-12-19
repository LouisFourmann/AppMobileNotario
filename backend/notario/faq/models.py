from django.db import models
from accounts.models import User

class Question(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, name, description, title):
        new_question = cls(name=name, description=description, title=title)
        return new_question
