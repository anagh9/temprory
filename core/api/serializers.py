from dataclasses import field
from rest_framework import serializers
from .models import Movie, Collection


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('uuid', 'title', 'description',
                  'genres')


class CollectionSerializer(serializers.ModelSerializer):
    collections = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ('uuid', 'collections')

    def get_is_success(self, obj):
        return True


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('genres',)
