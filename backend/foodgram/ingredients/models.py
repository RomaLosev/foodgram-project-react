from django.db import models
from django.core.validators import MinValueValidator

class Ingredient(models.Model):
    name = models.CharField(
        'наименование',
        max_length=100,
    )
    unit = models.CharField(
        'Единица измерения',
        max_length=200
    )
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class CountOfIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='count_in_recipes',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1, message='Количество ингридиентов не может быть меньше 1',)],
    )
