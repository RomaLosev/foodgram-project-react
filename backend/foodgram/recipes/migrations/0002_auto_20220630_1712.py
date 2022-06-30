# Generated by Django 3.2.13 on 2022-06-30 14:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='countofingredient',
            name='unique_ingredient_amount',
        ),
        migrations.AddField(
            model_name='countofingredient',
            name='recipe',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='recipes.recipe', verbose_name='Рецепт'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='countofingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Количество', validators=[django.core.validators.MinValueValidator(1, message='Не может быть меньше - 1')]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Время приготовления', validators=[django.core.validators.MinValueValidator(1, message='{MIN_VALUE_ERROR} - {MIN_VALUE}')]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Ингредиенты', related_name='recipes', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddConstraint(
            model_name='countofingredient',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_amount'),
        ),
    ]
