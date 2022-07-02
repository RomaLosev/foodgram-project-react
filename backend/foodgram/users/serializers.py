from rest_framework.serializers import SerializerMethodField, ModelSerializer
from djoser.serializers import UserCreateSerializer

from users.models import Follow, User
from recipes.models import Recipe


class CustomUserSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField(method_name='is_subscribed_user')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
            'is_subscribed',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def is_subscribed_user(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Follow.objects.filter(user=user, author=obj.id).exists()
        )


class ShortRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(CustomUserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = SerializerMethodField(method_name='get_recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
