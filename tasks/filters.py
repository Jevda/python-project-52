# tasks/filters.py
# Файл для определения класса фильтрации задач

from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

from .models import Task # Импортируем модель Task из текущего приложения
from statuses.models import Status # Импортируем модель Status из приложения statuses
from labels.models import Label # Импортируем модель Label из приложения labels
from django.contrib.auth.models import User # Импортируем стандартную модель User

# Определяем класс фильтра, наследуясь от FilterSet из django-filter
class TaskFilter(FilterSet):
    # Фильтр по статусу
    status = ModelChoiceFilter(
        queryset=Status.objects.all(), # Источник данных - все объекты Status
        label=_('Статус'), # Метка для поля в форме
        empty_label=_('Все статусы'), # Текст для пустого варианта (не фильтровать)
        # Добавляем CSS класс для стилизации виджета как в Bootstrap
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр по исполнителю
    executor = ModelChoiceFilter(
        queryset=User.objects.all(), # Источник данных - все объекты User
        label=_('Исполнитель'),
        empty_label=_('Все исполнители'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр по метке
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(), # Источник данных - все объекты Label
        label=_('Метка'),
        empty_label=_('Все метки'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр для отображения "только своих задач"
    self_tasks = BooleanFilter(
        field_name='author', # Указываем, что фильтровать будем по полю 'author' модели Task
        label=_('Только свои задачи'),
        # Указываем метод, который будет выполнять фильтрацию
        method='filter_self_tasks',
        # Используем виджет чекбокса
        widget=forms.CheckboxInput,
    )

    # Метод для кастомной фильтрации "только своих задач"
    def filter_self_tasks(self, queryset, name, value):
        # queryset - текущий набор задач
        # name - имя поля ('author')
        # value - значение чекбокса (True, если отмечен, False иначе)
        if value:
            # Если чекбокс отмечен, фильтруем задачи, где автор равен текущему пользователю
            # self.request доступен благодаря передаче request в FilterView
            return queryset.filter(author=self.request.user)
        # Если чекбокс не отмечен, возвращаем исходный queryset без изменений
        return queryset

    # Внутренний класс Meta для настройки FilterSet
    class Meta:
        model = Task # Указываем модель, для которой создается фильтр
        # Указываем поля модели, по которым будет происходить фильтрация
        # 'self_tasks' - это поле нашего BooleanFilter, оно не из модели
        fields = ['status', 'executor', 'labels', 'self_tasks']