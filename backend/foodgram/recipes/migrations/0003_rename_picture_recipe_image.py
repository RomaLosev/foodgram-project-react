# Generated by Django 3.2.13 on 2022-06-25 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220625_1835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='picture',
            new_name='image',
        ),
    ]
