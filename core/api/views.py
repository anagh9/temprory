from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
import collections
from django.db.models import Count
from .models import *
from .serializers import *
from rest_framework import routers, serializers, viewsets
import json
import requests
from django.shortcuts import HttpResponse
from django.views.generic import ListView
from django.http import JsonResponse
from django.conf import settings


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GetMovie(APIView):
    def get(self, request):
        r = requests.get(
            settings.BASE_URL, params=request.GET, auth=(settings.BASE_USERNAME, settings.BASE_PASSWORD))

        if r.status_code == 200:
            return Response(r.json())
        return Response({"msg": "Error Try Again"})


# class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.all()
    # serializer_class = MovieSerializer


class CollectionViewSet(viewsets.ViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True)
        queryset_genres = Movie.objects.values("genres").annotate(
            Count("genres")).order_by('-genres__count')[:3]
        genres_serializer = GenreSerializer(queryset_genres, many=True)
        return Response({
            "is_success": True,
            "data": {"collections": serializer.data},
            "favourite_genres": genres_serializer.data
        })

    def create(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        movies = request.data.get("movies")
        collection_serializer = CollectionSerializer(
            data={"title": title, "description": description})
        if collection_serializer.is_valid(raise_exception=True):
            collection_saved = collection_serializer.save()

        for _ in movies:
            title = _.get('title')
            description = _.get('description')
            genres = _.get('genres')
            movie_serializer = MovieSerializer(data={
                "title": title, "description": description, "genres": genres, "collections": collection_saved.uuid
            })
            if movie_serializer.is_valid(raise_exception=True):
                movie_saved = movie_serializer.save()

        return Response({"collection_uuid": movie_saved.uuid})

    def retrieve(self, request, pk=None):
        queryset = Collection.objects.filter(pk=pk).first()
        serializer = CollectionSerializer(queryset)
        movie_queryset = Movie.objects.filter(collections=pk).all()
        movie_serializer = MovieSerializer(movie_queryset, many=True)
        obj = dict()
        obj = serializer.data
        obj["movies"] = movie_serializer.data
        return Response(
            obj
        )

    def update(self, request, pk=None):
        queryset = Collection.objects.filter(pk=pk).first()
        # movie_queryset = Movie.objects.filter(collections=pk).all()
        # movie_serializer = MovieSerializer(movie_queryset, many=True)
        title = request.data.get("title")
        description = request.data.get("description")

        collection_serializer = CollectionSerializer(queryset,
                                                     data={"title": title, "description": description})

        if collection_serializer.is_valid(raise_exception=True):
            collection_serializer.save()

        return Response(collection_serializer.data)

    def destroy(self, request, pk=None):
        snippet = Collection.objects.filter(pk=pk).first()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""


 “title”: “<Title of the collection>”,
    “description”: “<Description of the collection>”,
    “movies”: [
        {
            “title”: <title of the movie>,
            “description”: <description of the movie>,
            “genres”: <generes>,
            “uuid”: <uuid>
        }, ...
    ]
"""
