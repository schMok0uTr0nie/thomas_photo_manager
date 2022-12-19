from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('photon.urls')),
    path('api/v1/', include('photon_api.urls'))
]
