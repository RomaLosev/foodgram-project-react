from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.core.validators import MinValueValidator

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(
        'тэг',
        max_length=30
    )
    color = models.CharField(
        'цвет в HEX формате',
        max_length=7
    )
    slug = models.SlugField(
        'слаг',
        max_length=30
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


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
        validators=[MinValueValidator(1,message='Количество ингридиентов не может быть меньше 1',)],
    )


class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=30
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
