from django.views import View
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from djoser.views import TokenCreateView, UserViewSet

from recipes.models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = (IsAdminOrReadOnly,)
