from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from photon.models import Person
from photon_api.serializers import PersonSerializer


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
