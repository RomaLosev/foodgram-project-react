from django.db import models
from django.urls import reverse
from foodgram.settings import MIN_VALUE, MIN_VALUE_ERROR
from users.models import User

from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(
        'наименование',
        max_length=100,
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(fields=('name', 'measurement_unit',),
                                    name='unique ingredient'),
        )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        help_text='тэг',
        max_length=30
    )
    color = models.CharField(
        verbose_name='Цвет',
        help_text='цвет в HEX формате',
        max_length=7
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='слаг',
        max_length=30
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class CountOfIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        help_text='Количество',
        verbose_name='Количество',
        validators=(
            MinValueValidator(
                MIN_VALUE,
                message=f'{MIN_VALUE_ERROR} - {MIN_VALUE}',
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепт'
        verbose_name_plural = 'Ингредиенты в рецепт'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'amount',),
                name='unique_ingredient_amount',
            ),
        )

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.amount}'
            f' ({self.ingredient.measurement_unit})'
        )


class Recipe(models.Model):
    name = models.CharField(
        help_text='Название рецепта',
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        help_text='Изображение готового блюда',
        verbose_name='Изображение'

    )
    text = models.TextField(
        help_text='Описание рецепта',
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        CountOfIngredient,
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Тэги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        help_text='Время приготовления',
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                1,
                message='{MIN_VALUE_ERROR} - {MIN_VALUE}',
            ),
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name} ({self.author})'

    def get_absoulute_url(self):
        return reverse('recipe', args=[self.pk])


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_user',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(fields=('user', 'recipe',),
                                    name='unique favorite'),
        )

    def __str__(self):
        return f'{self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = (
            models.UniqueConstraint(fields=('user', 'recipe',),
                                    name='unique shopping cart'),
        )

    def __str__(self):
        return f'{self.recipe}'
