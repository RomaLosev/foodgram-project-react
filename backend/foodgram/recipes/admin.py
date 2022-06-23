from django.contrib import admin

from .models import Ingredient, Recipe

@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    search_fields = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit',
    )
    search_fields = ('name',)