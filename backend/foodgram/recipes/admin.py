from django.contrib import admin

from .models import Recipe

@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    search_fields = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
