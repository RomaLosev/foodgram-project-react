from django.contrib.auth.hashers import make_password
from rest_framework.serializers import SerializerMethodField
from djoser.serializers import UserCreateSerializer

from recipes.serializers import RecipeShortReadSerializer
from recipes.models import User


class UserSerializer(UserCreateSerializer):
    # is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def create(self, validated_data):
        validated_data['password'] = (
            make_password(validated_data.pop('password'))
        )
        return super().create(validated_data)

    # def is_subscribed_user(self, obj):
    #     user = self.context['request'].user
    #     return (
    #         user.is_authenticated
    #         and obj.subscribing.filter(user=user).exists()
    #     )

class SubscriptionSerializer(UserSerializer):
    recipes = RecipeShortReadSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()