# tasks/filters.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

from .models import Task
from statuses.models import Status
from labels.models import Label

# Кастомный класс поля формы (оставляем)
class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

# Класс Фильтра
class TaskFilter(FilterSet):
    # Фильтр по статусу
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('Все статусы'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
    # Используем ModelChoiceFilter + field_class + ЯВНЫЙ widget
    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        field_class=UserChoiceField, # Используем наш класс для логики отображения
        label=_('Исполнитель'),
        empty_label=_('Все исполнители'),
        # !!! Возвращаем явное указание виджета !!!
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # --- КОНЕЦ ИЗМЕНЕНИЯ ---

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

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task # Используем класс модели
        fields = ['status', 'executor', 'labels', 'self_tasks']
