# Generated by Django 3.2.13 on 2022-07-04 19:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220703_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='countofingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Количество', validators=[django.core.validators.MinValueValidator(1, message='Не может быть меньше - 1')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Время приготовления', validators=[django.core.validators.MinValueValidator(1, message='{MIN_VALUE_ERROR} - {MIN_VALUE}')], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Изображение готового блюда', upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Название рецепта', max_length=200, verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Описание рецепта', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='цвет в HEX формате', max_length=7, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='тэг', max_length=30, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='слаг', max_length=30, verbose_name='Слаг'),
        ),
    ]