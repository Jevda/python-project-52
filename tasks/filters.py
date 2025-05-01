# tasks/filters.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Импортируем нужные классы фильтров
from django_filters import (
    BooleanFilter,
    ChoiceFilter,
    FilterSet,
    ModelChoiceFilter,
)

from labels.models import Label
from statuses.models import Status

from .models import Task


# Класс Фильтра
class TaskFilter(FilterSet):

    # --- ИЗМЕНЕНИЕ ЗДЕСЬ: Добавляем empty_label ---
    executor = ChoiceFilter(
        label=_("Исполнитель"),
        # !!! Указываем текст для пустого значения здесь !!!
        empty_label=_("Все исполнители"),
        # Choices будут заданы в __init__ ниже
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    # --- КОНЕЦ ИЗМЕНЕНИЯ ---

    # Фильтр по статусу
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Статус"),
        empty_label=_("Все статусы"),  # ModelChoiceFilter также использует empty_label
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Фильтр по метке
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Метка"),
        empty_label=_("Все метки"),  # ModelChoiceFilter также использует empty_label
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Фильтр "Только свои задачи"
    self_tasks = BooleanFilter(
        field_name="author",
        label=_("Только свои задачи"),
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
    )

    # Метод __init__ для генерации choices для executor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # --- ИЗМЕНЕНИЕ ЗДЕСЬ: Убираем ручное добавление пустого варианта ---
        # Формируем список ТОЛЬКО из пользователей: (pk, full_name)
        executor_choices = [
            (user.pk, user.get_full_name())
            for user in User.objects.order_by("first_name", "last_name")
        ]
        # --- КОНЕЦ ИЗМЕНЕНИЯ ---
        # Присваиваем сформированный список полю choices нашего фильтра executor
        self.filters["executor"].field.choices = executor_choices
        # Примечание: Django автоматически добавит вариант, указанный в empty_label

    def filter_self_tasks(self, queryset, name, value):
        if value:
            if hasattr(self, "request") and self.request.user.is_authenticated:
                return queryset.filter(author=self.request.user)
            return queryset.none()
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]
