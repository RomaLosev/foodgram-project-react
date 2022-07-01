from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from foodgram.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('api.urls')),
    path('api/', include('djoser.urls')),
]
