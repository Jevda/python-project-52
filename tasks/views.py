# tasks/views.py
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView

from .models import Task
from .forms import TaskForm
from .filters import TaskFilter


class TasksIndexView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    # --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
    # Метод для передачи request в фильтр
    def get_filterset_kwargs(self, filterset_class): # Добавляем filterset_class как аргумент
        # Получаем стандартные аргументы для filterset, передавая filterset_class
        kwargs = super().get_filterset_kwargs(filterset_class)
        # Добавляем объект request в эти аргументы
        kwargs['request'] = self.request
        # Возвращаем обновленные аргументы
        return kwargs
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    success_message = "Задача успешно изменена"


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = "Задача успешно удалена"

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только её автор")
        return redirect('tasks:index')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
