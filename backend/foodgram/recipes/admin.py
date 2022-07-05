from django.contrib import admin
from recipes.models import Favorite

from recipes.models import (
    Ingredient, Recipe,
    Tag, CountOfIngredient,
    Favorite, ShoppingCart
)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user__username', 'recipe__name', 'user__email')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user__username', 'recipe__name', 'user__email')
    list_filter = ('user',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
        'id',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(CountOfIngredient)
class CountOfIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'amount',
    )
    search_fields = ('ingredient',)


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'favorite_count',
    )
    list_filter = ('tags',)
    search_fields = ('name', 'author__username', 'author__email')
    empty_value_display = '-пусто-'

    @admin.display(
        empty_value='0',
        description='Сколько раз добавили в избранное'
    )
    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj.id).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    search_fields = ('name',)
