from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views
from djoser import views as djoser_views

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet, basename='users')

authorization = [
    path(
        'token/login/',
        djoser_views.TokenCreateView.as_view(),
        name='login'
    ),
    path(
        'token/logout/',
        djoser_views.TokenDestroyView.as_view(),
        name='login'
    ),
]

urlpatterns = [
    url(r'', include(router.urls)),
    path('auth/', include(authorization)),
]