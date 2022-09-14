from rest_framework import serializers
from .models import Collection
from django.contrib.auth.models import User


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ('uuid', 'title', 'description',)


class CollectionSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('uuid', 'title', 'description', 'movies')

    def create(self, validated_data):
        request = self.context.get("request.user")
        collection = Collection()
        collection.user = request   
        collection.title = validated_data['title']
        collection.description = validated_data['description']
        collection.movies = validated_data['movies']
        collection.save()
        return collection

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.movies = validated_data.get('movies', instance.movies)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        return User.objects.create(**validated_data)
