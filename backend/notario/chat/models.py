from django.db import models
from accounts.models import User

class Chat(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_one")
    user_two = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_two")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True)
    read = models.BooleanField(default=False)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
