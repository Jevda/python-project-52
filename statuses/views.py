# statuses/views.py
# Импортируем систему сообщений и редирект
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# Импортируем ошибку ProtectedError
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


# Представление для списка статусов
class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"

# Представление для СОЗДАНИЯ статуса
class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:index")
    success_message = "Статус успешно создан"

# Представление для РЕДАКТИРОВАНИЯ статуса
class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:index")
    success_message = "Статус успешно изменен"

# Представление для УДАЛЕНИЯ статуса
class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:index")
    # Сообщение об успехе будет добавлено вручную при успешном удалении
    # success_message = "Статус успешно удален" # Убираем авто-сообщение

    # --- ИЗМЕНЕНИЕ ЗДЕСЬ: Переопределяем метод post для обработки ProtectedError ---
    def post(self, request, *args, **kwargs):
        try:
            # Пытаемся выполнить стандартное удаление из DeleteView
            response = super().delete(request, *args, **kwargs)
            # Если удаление прошло успешно (не было ProtectedError),
            # добавляем сообщение об успехе вручную
            messages.success(self.request, "Статус успешно удален")
            return response
        except ProtectedError:
            # Если возникла ошибка ProtectedError (статус используется)
            # Показываем сообщение об ошибке
            messages.error(
                self.request,
                "Невозможно удалить статус, потому что он используется",
            )
            # Делаем редирект обратно на список статусов
            return redirect(self.success_url)
    # --- КОНЕЦ ИЗМЕНЕНИЯ ---
