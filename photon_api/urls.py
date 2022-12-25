from django.urls import path
from .views import *

urlpatterns = [
    path('snap/list', SnapAPIView.as_view(), name="api_snaplist"),
    path('cat/list', CatAPIView.as_view(), name="api_catlist"),
    path('person/list', PersonAPIView.as_view(), name="api_people"),
    path('cam/list', CamAPIView.as_view(), name="api_camlist"),
    path('prof/list', ProfAPIView.as_view(), name="api_proflist")
]
