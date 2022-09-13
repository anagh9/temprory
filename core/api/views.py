from collections import Counter
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
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({'access_token': str(refresh.access_token)})


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
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Collection.objects.filter(user=request.user).all()
        serializer = CollectionSerializer(queryset, many=True)
        favorite_genres = []
        count = {}
        for _ in queryset:
            for movie in _.movies:
                print(movie)
                print("#83", movie.get("genres"))
                if len(movie["genres"]) < 1:
                    continue
                genres = movie["genres"].split(",")
                for genre in genres:
                    if count.get(genre):
                        count[genre] = count[genre]+1
                    else:
                        count[genre] = 1
                # genres = max(count, key=count.get)
                # print("#76",genres)
                # favorite_genres.append(genres)
        print(count)

        k = Counter(count)
        high = k.most_common(3)
        for i in high:
            favorite_genres.append(i[0])
        return Response({
            "is_success": True,
            "data": {"collections": serializer.data},
            "favorite_genres": favorite_genres,
        })

    def create(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        movies = request.data.get("movies")
        user = request.user
        collection = Collection(
            title=title, description=description, movies=movies, user=user)
        collection.save()
        # if collection_serializer.is_valid(raise_exception=True):
        # collection_saved = collection_serializer.save()

        # obj = collection.save()
        # print("#78", collection.uuid)
        collection_serializer = CollectionSingleSerializer(collection)

        return Response({"collection_uuid": collection_serializer.data.get("uuid")})

    def retrieve(self, request, pk=None):
        queryset = Collection.objects.filter(pk=pk, user=request.user).first()
        serializer = CollectionSingleSerializer(queryset)
        obj = dict()
        obj = serializer.data
        return Response(
            obj
        )

    def update(self, request, pk=None):
        queryset = Collection.objects.filter(pk=pk, user=request.user).first()
        title = request.data.get("title")
        description = request.data.get("description")
        movies = request.data.get("movies")

        if title is not None:
            queryset.title = title
        if description is not None:
            print("#125")
            queryset.description = description
        if movies is not None:
            queryset.movies = movies

        obj = queryset.save()
        collection_serializer = CollectionSerializer(queryset)
        return Response(collection_serializer.data)

    def destroy(self, request, pk=None):
        snippet = Collection.objects.filter(pk=pk, user=request.user).first()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestCount(APIView):
    def get(self, request):
        q = Count.objects.all().first()
        counter = q.counter
        return Response({"requests": counter})

    def post(self, request):
        q = Count.objects.all().first()
        q.counter = 0
        q.save()
        return Response({"message": "request count reset successfully"})


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
