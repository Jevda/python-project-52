# tasks/filters.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Импортируем ChoiceFilter вместо ModelChoiceFilter для executor
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter, ChoiceFilter

from .models import Task
from statuses.models import Status
from labels.models import Label

# Убираем импорт UserChoiceField, он здесь не нужен
# from .forms import UserChoiceField

# Класс Фильтра
class TaskFilter(FilterSet):

    # --- ИСПОЛЬЗУЕМ ChoiceFilter для executor ---
    executor = ChoiceFilter(
        label=_('Исполнитель'),
        # Choices будут заданы в __init__ ниже
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр по статусу (остается ModelChoiceFilter)
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('Все статусы'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Фильтр по метке (остается ModelChoiceFilter)
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

    # --- Добавляем __init__ для генерации choices ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Формируем список вариантов для исполнителя: (pk, full_name)
        # Добавляем пустой вариант в начало
        executor_choices = [('', _('Все исполнители'))] + [
            (user.pk, user.get_full_name()) for user in User.objects.order_by('first_name', 'last_name') # Добавим сортировку
        ]
        # Присваиваем сформированный список полю choices нашего фильтра executor
        self.filters['executor'].field.choices = executor_choices

    def filter_self_tasks(self, queryset, name, value):
        if value:
            if hasattr(self, 'request') and self.request.user.is_authenticated:
                 return queryset.filter(author=self.request.user)
            return queryset.none()
        return queryset

    class Meta:
        model = Task
        # Указываем поля модели ИЛИ имена наших полей фильтра
        fields = ['status', 'executor', 'labels', 'self_tasks']
