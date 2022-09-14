from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'collection', CollectionViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path("movies/", GetMovie.as_view()),
    path('register/', RegisterUser.as_view()),
    path('request-count/', RequestCount.as_view()),
    path('request-count/reset/', RequestCount.as_view()),
]
