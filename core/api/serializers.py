from dataclasses import field
from rest_framework import serializers
from .models import Movie, Collection
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('uuid', 'title', 'description',
                  'genres', 'collections')

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    # collections = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ('uuid', 'title', 'description')

    def create(self, validated_data):
        return Collection.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('genres',)

class UserSerializer(serializers.ModelSerializer):
    # collections = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        return User.objects.create(**validated_data)
