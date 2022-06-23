from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe


class RecipeSerializer(ModelSerializer):
    model = Recipe
    class Meta:
        model = Recipe
        fields = '__all__'

class ShortRecipeSerializer(ModelSerializer):
    model = Recipe
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)