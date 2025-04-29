# task_manager/views.py
# Файл для представлений (views) основного приложения task_manager

from django.http import HttpResponse

# Простое представление, которое возвращает текстовый ответ
def index(request):
    # Возвращаем HTTP-ответ с текстом приветствия
    return HttpResponse("Это менеджер задач от Хекслет")
