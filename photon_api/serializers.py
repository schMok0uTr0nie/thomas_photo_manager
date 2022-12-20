from rest_framework import serializers
from photon.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name')




# class HotelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hotel
#
#         fields = ("id", "name", "address", "location")
#
#         extra_kwargs = {"location": {"read_only": True}}