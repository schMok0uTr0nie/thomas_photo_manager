from django.urls import path
from .views import *

urlpatterns = [
    path('people', PersonAPIView.as_view(), name="api_people")
]
