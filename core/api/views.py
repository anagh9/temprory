from collections import Counter
from rest_framework import status
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
            try:
                serializer = UserSerializer(data=request.data)
                print(serializer)

                if serializer.is_valid():
                    serializer.save()
                user = User.objects.get(username=serializer.data['username'])
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token)})

            except Exception as e:
                return Response({'message': 'Username and Password is required'}, status = status.HTTP_400_BAD_REQUEST)


class GetMovie(APIView):
    def get(self, request):
        r = requests.get(
            settings.BASE_URL, auth=(settings.BASE_U, settings.BASE_PASSWORD))

        if r.status_code == 200:
            return Response(r.json())
        return Response({"msg": r})

class CollectionViewSet(viewsets.ViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        try:
            queryset = Collection.objects.filter(user=request.user).all()
            if queryset:
                serializer = CollectionSerializer(queryset, many=True)
                favorite_genres = []
                count = {}
                print(queryset)
                for _ in queryset:
                    for movie in _.movies:
                        if len(movie["genres"]) < 1:
                            continue
                        genres = movie["genres"].split(",")
                        count = CollectionViewSet.genres_dict(genres)
                k = Counter(count)
                high = k.most_common(3)
                for i in high:
                    favorite_genres.append(i[0])
                return Response({
                    "is_success": True,
                    "data": {"collections": serializer.data},
                    "favorite_genres": favorite_genres,
                })
            else:
                return Response({'message':'Collection Not found'}, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        

    @staticmethod
    def genres_dict(genres):
        count ={}
        for genre in genres:
            if count.get(genre):
                count[genre] = count[genre]+1
            else:
                count[genre] = 1
        return count

    def create(self, request):
        try:
            title = request.data.get("title")
            description = request.data.get("description")
            movies = request.data.get("movies")
            user = request.user
            collection = Collection(
                title=title, description=description, movies=movies, user=user)
            collection.save()
            collection_serializer = CollectionSingleSerializer(collection)
            return Response({"collection_uuid": collection_serializer.data.get("uuid")}, status= status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            queryset = Collection.objects.filter(pk=pk, user=request.user).first()
            if queryset:
                serializer = CollectionSingleSerializer(queryset)
                obj = dict()
                obj = serializer.data
                return Response(
                    obj
                )
            else:
                return Response({'message':'Collection Not found'}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

        

    def update(self, request, pk=None):
        try:
            queryset = Collection.objects.filter(pk=pk, user=request.user).first()
            if queryset:
                title = request.data.get("title")
                description = request.data.get("description")
                movies = request.data.get("movies")

                if title is not None:
                    queryset.title = title
                if description is not None:
                    queryset.description = description
                if movies is not None:
                    queryset.movies = movies

                obj = queryset.save()
                collection_serializer = CollectionSerializer(queryset)
                return Response(collection_serializer.data)
            else:
                return Response({'message':'Collection Not found'}, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            snippet = Collection.objects.filter(pk=pk, user=request.user).first()
            if snippet:
                snippet.delete()
                return Response({'message' :'Collection deleted'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Collection not found'}, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message' : str(e)}, status = status.HTTP_400_BAD_REQUEST)


class RequestCount(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        try:
            if request.method == 'GET':
                q = Count.objects.all().first()
                counter = q.counter
                return Response({"requests": counter})
            else:
                return Response({'message' : 'Method not allowed'}, status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message' : str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if request.method == 'POST':
                q = Count.objects.all().first()
                q.counter = 0
                q.save()
                return Response({"message": "request count reset successfully"})
            else:
                return Response({'message' : 'Method not allowed'}, status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message' : str(e)}, status = status.HTTP_400_BAD_REQUEST)

