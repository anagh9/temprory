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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        r = requests.get(
            'https://demo.credy.in/api/v1/maya/movies/', params=request.GET)
        if r.status_code == 200:
            return Response(r.json())
        return HttpResponse('Could not save data')


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CollectionViewSet(viewsets.ModelViewSet):

    def list(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True)
        queryset_genres = Movie.objects.values("genres").annotate(
            Count("genres")).order_by('-genres__count')[:3]
        genres_serializer = GenreSerializer(queryset_genres, many=True)
        return Response({
            "is_success": True,
            "data": serializer.data,
            "favourite_genres": genres_serializer.data
        })

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
