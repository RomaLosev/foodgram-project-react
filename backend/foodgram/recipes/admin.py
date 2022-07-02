from django.contrib import admin
from recipes.models import Favorite

from recipes.models import Ingredient, Recipe, Tag, CountOfIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit',
        'id',
    )
    search_fields = ('name', 'id')


@admin.register(CountOfIngredient)
class CountOfIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'amount',
    )
    search_fields = ('ingredient',)


class CountOfIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (
        CountOfIngredientInline,
    )
    list_display = (
        'name',
        'author',
        'favorite_count',
    )
    search_fields = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    @admin.display(empty_value='0')
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
