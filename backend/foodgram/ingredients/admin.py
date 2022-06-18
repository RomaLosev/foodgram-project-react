from django.contrib import admin

from .models import Ingredient

@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit',
    )
    search_fields = ('name', 'unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
