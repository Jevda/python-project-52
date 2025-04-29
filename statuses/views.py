# statuses/views.py
# Файл для представлений приложения statuses

# Добавляем DeleteView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
# Пока не нужно:
# from django.contrib import messages

# Импортируем модель Status и форму StatusForm
from .models import Status
from .forms import StatusForm

# Представление для списка статусов
class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

# Представление для СОЗДАНИЯ статуса
class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = "Статус успешно создан"

# Представление для РЕДАКТИРОВАНИЯ статуса
class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = "Статус успешно изменен"

# --- Новое представление для УДАЛЕНИЯ статуса ---
class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status                  # Используем модель Status
    template_name = 'statuses/delete.html' # Шаблон подтверждения удаления
    success_url = reverse_lazy('statuses:index') # URL для редиректа после успеха
    success_message = "Статус успешно удален" # Flash-сообщение

    # TODO: Позже добавить сюда проверку, связан ли статус с задачами
    # (переопределив метод post или delete и вызвав ProtectedError
    # или вернув ошибку/редирект с сообщением)
