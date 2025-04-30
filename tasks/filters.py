# tasks/filters.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Импортируем FilterSet и нужные типы фильтров
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

from .models import Task
from statuses.models import Status
from labels.models import Label

# --- Кастомный класс ПОЛЯ ФОРМЫ (оставляем) ---
# Этот класс отвечает за логику отображения полного имени
class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

# --- Класс Фильтра ---
class TaskFilter(FilterSet):
    # Фильтр по статусу (как был)
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('Все статусы'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
    # Используем стандартный ModelChoiceFilter, но указываем field_class
    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        # !!! Указываем, что для рендеринга поля формы нужно использовать наш UserChoiceField !!!
        field_class=UserChoiceField,
        label=_('Исполнитель'), # Метка для фильтра
        empty_label=_('Все исполнители'),
        # Виджет можно не указывать здесь, т.к. он будет взят из UserChoiceField
        # widget=forms.Select(attrs={'class': 'form-select'}),
    )
    # --- КОНЕЦ ИЗМЕНЕНИЯ ---

    # Фильтр по метке (как был)
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Метка'),
        empty_label=_('Все метки'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр "Только свои задачи" (как был)
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
