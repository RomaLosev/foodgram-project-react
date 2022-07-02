from rest_framework.serializers import SerializerMethodField, ModelSerializer
from djoser.serializers import UserCreateSerializer

from users.models import Follow, User
from recipes.models import Recipe


class CustomUserSerializer(UserCreateSerializer):
    is_following = SerializerMethodField(method_name='is_following_user')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
            'is_following',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def is_following_user(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Follow.objects.filter(user=user, author=obj.id).exists()
        )


class ShortRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(CustomUserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = SerializerMethodField(
        read_only=True, method_name='recipes_count'
    )

    def recipes_count(self, obj):
        return obj.recipes.count()

    class Meta(CustomUserSerializer.Meta):
        fields = ('recipes',)
