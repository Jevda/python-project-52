# tasks/filters.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

# !!! ШАГ 1: Возвращаем импорт Task !!!
from .models import Task
from statuses.models import Status
from labels.models import Label

# Кастомный класс поля для выбора пользователя (оставляем)
class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

# Класс фильтра
class TaskFilter(FilterSet):
    # Фильтр по статусу
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('Все статусы'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Используем UserChoiceField для исполнителя
    executor = UserChoiceField(
        queryset=User.objects.all(),
        label=_('Исполнитель'), # Используем явную метку
        empty_label=_('Все исполнители'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр по метке
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Метка'),
        empty_label=_('Все метки'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр "Только свои задачи"
    self_tasks = BooleanFilter(
        field_name='author',
        label=_('Только свои задачи'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput,
    )

    # Метод для фильтрации "Только свои задачи"
    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        # !!! ШАГ 2: Указываем класс модели, а не строку !!!
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
