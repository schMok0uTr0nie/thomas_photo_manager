from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from .filters import *
from photon_api.serializers import *


class PersonAPIView(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'id': ['exact'],
        'name': ['icontains']
    }
    search_fields = {
        'id': ['exact'],
        'name': ['icontains']
    }
    ordering_fields = ['id', 'name']


class SnapAPIView(ListAPIView):
    queryset = Snapshot.objects.filter(author__profile__private=False)
    serializer_class = SnapSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'id': ['exact'],
        'category': ['exact'],
        'country': ['exact']
    }
    search_fields = {
        'id': ['exact'],
        'author': ['icontains'],
        'category': ['exact'],
        'person': ['icontains'],
        'camera': ['exact'],
        'city': ['icontains'],
        'region': ['icontains']
    }
    ordering_fields = ['id', 'author', 'category', 'country']


class CatAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'id': ['in'],
        'snap_count': ['gte']
    }
    search_fields = {
        'id': ['exact'],
        'name': ['icontains'],
    }
    ordering_fields = ['id', 'name', 'snap_count']


class CamAPIView(ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = CamSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'id': ['exact'],
        'snap_count': ['gte']
    }
    search_fields = {
        'id': ['exact'],
        'brand': ['icontains'],
    }
    ordering_fields = ['id', 'brand', 'snap_count']


class ProfAPIView(ListAPIView):
    queryset = Profile.objects.filter(private=False)
    serializer_class = ProfSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'city': ['exact'],
        'gear': ['exact'],
        'gender': ['exact'],
        'skill': ['exact'],
    }
    search_fields = {
        'id': ['exact'],
        'nick': ['icontains'],
        'fio': ['icontains'],
        'city': ['icontains']
    }
    ordering_fields = ['id', 'nick', 'skill', 'private']
