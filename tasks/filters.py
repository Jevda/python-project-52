# tasks/filters.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Импортируем нужные классы из django-filter
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

from .models import Task
from statuses.models import Status
from labels.models import Label

# Убираем кастомный класс UserChoiceField отсюда

# Класс Фильтра
class TaskFilter(FilterSet):
    # Используем СТАНДАРТНЫЙ ModelChoiceFilter для всех полей

    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('Все статусы'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    executor = ModelChoiceFilter( # <-- Стандартный ModelChoiceFilter
        queryset=User.objects.all(),
        label=_('Исполнитель'),
        empty_label=_('Все исполнители'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

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

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
