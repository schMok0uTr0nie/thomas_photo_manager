import django_filters
from django import forms
from django.db.models import Q
from django_filters import DateFilter

from .models import Snapshot


class SnapshotFilter(django_filters.FilterSet):
    datetime__gte = DateFilter(field_name='timestamp', lookup_expr='date__gte', widget=forms.DateInput(), label="От (дата)")
    datetime__lte = DateFilter(field_name='timestamp', lookup_expr='date__lte', widget=forms.DateInput(), label="До (дата)")

    location = django_filters.CharFilter(method='location_filter', label="Город/Регион/Страна")

    class Meta:
        model = Snapshot

        fields = {
            'id': ['exact'],
            'author': ['exact'],
            'category': ['exact'],
            'camera': ['exact'],
        }

    def location_filter(self, queryset, name, value):
        return queryset.filter(Q(city__icontains=value) | Q(region__icontains=value) | Q(country__icontains=value))


class PortfolioFilter(django_filters.FilterSet):
    datetime__lte = DateFilter(field_name='timestamp', lookup_expr='date__lte')
    location = django_filters.CharFilter(method='location_filter', label="Город/Регион/Страна")

    class Meta:
        model = Snapshot
        fields = {
            'id': ['exact'],
            'category': ['exact'],
            'camera': ['exact'],
        }


class CatSelectedFilter(django_filters.FilterSet):
    datetime__gte = DateFilter(field_name='timestamp', lookup_expr='date__gte', widget=forms.DateInput(),
                               label="От (дата)")
    datetime__lte = DateFilter(field_name='timestamp', lookup_expr='date__lte', widget=forms.DateInput(),
                               label="До (дата)")

    class Meta:
        model = Snapshot
        fields = {
            'id': ['exact'],
            'author': ['exact'],
            'camera': ['exact'],
        }
