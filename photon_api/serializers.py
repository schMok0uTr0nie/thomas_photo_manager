from rest_framework import serializers
from photon.models import *


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name')


class SnapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('id', 'author', 'photo', 'category', 'description',
                  'person', 'camera', 'city', 'region', 'country', 'timestamp')


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'snap_count')


class CamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'brand', 'snap_count')


class ProfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'nick', 'fio', 'contacts', 'gear', 'skill', 'gender', 'city')
