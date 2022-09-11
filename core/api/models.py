from django.db import models
import uuid


class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Movie(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=100)
    collections = models.ForeignKey(
        Collection, related_name='collections', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
