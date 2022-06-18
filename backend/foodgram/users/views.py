from rest_framework import viewsets

from recipes.models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = (IsAdminOrReadOnly,)
