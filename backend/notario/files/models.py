from django.db import models
from accounts.models import User

class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='CustomerFile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, owner, name, file):
        new_file = cls(owner=owner, name=name, file=file)
        return new_file
