from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction

from foodgram.settings import MIN_AMOUNT, MIN_COOCKING_TIME
from recipes.models import Recipe, Tag, Ingredient, CountOfIngredient, Favorite, ShoppingCart
from users.serializers import CustomUserSerializer, ShortRecipeSerializer

class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов
    """
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')
        read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов
    """
    class Meta:
        model = Ingredient
        fields = ('name', 'unit')
        read_only_fields = '__all__',


class CountOfIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода количества ингредиентов
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(
        source='ingredient.unit'
    )

    class Meta:
        model = CountOfIngredient
        fields = ('id', 'name', 'unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = CountOfIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True, method_name='is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True, method_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = '__all__'


    def is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()
    
class AddIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления Ингредиентов
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = CountOfIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления рецептов
    """
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time')

    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты должны быть уникальными!'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= MIN_AMOUNT:
                raise serializers.ValidationError({
                    'amount': 'Количество ингредиентов должно быть больше {MIN_AMOUNT}!'
                })

        tags = data['tags']
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать хотя бы один тэг!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'Тэги должны быть уникальными!'
                })
            tags_list.append(tag)

        cooking_time = data['cooking_time']
        if int(cooking_time) <= MIN_COOCKING_TIME:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть больше {MIN_COOCKING_TIME}!'
            })
        return data

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            CountOfIngredient.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.tags.clear()
        CountOfIngredient.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка избранного
    """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        #recipe = data['recipe']
        # if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
        #     raise serializers.ValidationError({
        #         'status': 'Рецепт уже есть в избранном!'
        #     })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка покупок
    """
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe']
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data
