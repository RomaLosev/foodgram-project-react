from django.contrib.auth.hashers import make_password
from rest_framework.serializers import SerializerMethodField
from djoser.serializers import UserCreateSerializer
from .models import Follow

from recipes.serializers import ShortRecipeSerializer
from users.models import User


class UserSerializer(UserCreateSerializer):
    is_following = SerializerMethodField('is_following_user')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
            'is_following',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    # def create(self, validated_data):
    #     validated_data['password'] = (
    #         make_password(validated_data.pop('password'))
    #     )
    #     return super().create(validated_data)

    def is_following_user(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Follow.objects.filter(user=user, author=obj.id).exists()
        )

class SubscriptionSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()