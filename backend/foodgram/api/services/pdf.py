import io
import os
from typing import TextIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import BASE_DIR

DATA_ROOT = os.path.join(BASE_DIR, 'backend/data')


def create_pdf(data: list, title: str) -> TextIO:
    """
    Создает pdf-файл
    """
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(
        TTFont(
            'CenturyGothic',
            'data/CenturyGothic.ttf',
            'UTF-8'
        )
    )

    page.setFont('CenturyGothic', size=24)
    height = 750
    page.drawString(55, height, f'{title}')
    page.setFont('CenturyGothic', size=18)
    height -= 30
    for i in data:
        page.drawString(
            15, height,
            (f"{i['ingredient__name']} - "
             f"{i['amount__sum']} "
             f"{i['ingredient__measurement_unit']}")
        )
        height -= 25

    page.showPage()
    page.save()
    buffer.seek(0)

    return buffer
