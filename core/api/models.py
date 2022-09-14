from django.db import models
from django.contrib.auth.models import User
import uuid


class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.JSONField()
    def __str__(self) -> str:
        return self.title

class Count(models.Model):
    
    counter = models.IntegerField(default=0)