import csv
import os

from foodgram import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'backend/data')


class Command(BaseCommand):
    """
    Добавляем ингредиенты из файла CSV
    """
    help = 'loading ingredients from data in json or csv'

    def handle(self, *args, **options):
        try:
            with open('data/ingredients.csv',
                      encoding='utf-8') as file:
                data = csv.reader(file)
                for row in data:
                    name, unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        unit=unit
                    )
        except FileNotFoundError:
            raise CommandError('Файл ingredients не найден')

app = Command()
app.handle()
print('Загрузка ингредиентов завершена')