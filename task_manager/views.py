from django.shortcuts import render
from django.utils import translation


def index(request):
    # Активируем русский язык при каждом запросе
    translation.activate('ru')
    if hasattr(request, 'LANGUAGE_CODE'):
        request.LANGUAGE_CODE = 'ru'
    return render(request, "index.html")