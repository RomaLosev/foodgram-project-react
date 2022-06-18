from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.core.validators import MinValueValidator

from tags.models import Tag
from ingredients.models import CountOfIngredient

User = get_user_model()

class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    picture = models.ImageField('Изображение готового блюда')
    description = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        CountOfIngredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(
            1,
            message='Время приготовления не может быть меньше минуты',
        ),)
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор',
    )
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.name} ({self.author})'

    def get_absoulute_url(self):
        return reverse('recipe', args=[self.pk])
