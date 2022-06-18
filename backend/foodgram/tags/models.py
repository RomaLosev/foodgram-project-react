from django.db import models

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
