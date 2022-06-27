from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from rest_framework import status
from .models import Follow
from djoser.views import UserViewSet

from recipes.models import User
from users.serializers import SubscriptionSerializer, CustomUserSerializer
from api.permissions import IsAdminOrReadOnly


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Отдаёт все подписки пользователя
    """
    serializer_class = SubscriptionSerializer(many=True)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(
            username=self.request.user)


class UsersViewSet(UserViewSet):
    """
    Отдаёт список пользователей
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    permission_classes = (IsAdminOrReadOnly,)


class FollowViewSet(views.APIView):
    """
    Обрабатывает подписки
    post/delete
    """
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Follow.objects.all()

    def post(self, request, pk):
        author = get_object_or_404(User, id=pk)
        if request.user == author:
            return Response(
                {'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.get_or_create(
            user=request.user,
            author=author,
        )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, id=pk)
        try:
            Follow.objects.get(
                user=request.user,
                author=author,
            ).delete()
        except Follow.DoesNotExist:
            return Response(
                {'Вы не были подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {f'Вы отписались от {author}'},
            status=status.HTTP_204_NO_CONTENT,
        )
