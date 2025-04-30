# task_manager/views.py
"""Views for the main task_manager application."""

# Импортируем функцию 'render' вместо 'HttpResponse'
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Представление для главной страницы
def index(request: HttpRequest) -> HttpResponse:
    """Render the main index page.

    Args:
        request: The HttpRequest object.

    Returns:
        The rendered HttpResponse for the index page.

    """
    # Используем функцию render()
    # Первый аргумент - объект запроса (request)
    # Второй аргумент - путь к файлу шаблона ('index.html')
    # Django будет искать 'index.html' в папке 'templates'
    return render(request, "index.html")
