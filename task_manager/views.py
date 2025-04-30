# task_manager/views.py
# Файл для представлений (views) основного приложения task_manager

# Импортируем функцию 'render' вместо 'HttpResponse'
from django.shortcuts import render


# Представление для главной страницы
def index(request):
    # Используем функцию render()
    # Первый аргумент - объект запроса (request)
    # Второй аргумент - путь к файлу шаблона ('index.html')
    # Django будет искать 'index.html' в папке 'templates'
    return render(request, "index.html")
