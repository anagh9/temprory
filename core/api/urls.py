from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'm', MovieViewSet)
router.register(r'collection', CollectionViewSet)

urlpatterns = [
    # path("register/", Register.as_view(), name="register"),

    path(r'', include(router.urls)),
    path("movies/", GetMovie.as_view(), name="get-movie"),
]
