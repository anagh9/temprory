from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'collection', CollectionViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path("movies/", GetMovie.as_view(), name="get-movie"),
]
