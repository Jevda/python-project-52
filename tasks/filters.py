from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_filters import (
    BooleanFilter,
    ChoiceFilter,
    FilterSet,
    ModelChoiceFilter,
)
from labels.models import Label
from statuses.models import Status
from .models import Task


class TaskFilter(FilterSet):

    executor = ChoiceFilter(
        label=_("Executor"),
        empty_label=_("All executors"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
        empty_label=_("All statuses"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        empty_label=_("All labels"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    self_tasks = BooleanFilter(
        field_name="author",
        label=_("Only my tasks"),
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executor_choices = [
            (user.pk, user.get_full_name())
            for user in User.objects.order_by("first_name", "last_name")
        ]
        self.filters["executor"].field.choices = executor_choices

    def filter_self_tasks(self, queryset, name, value):
        if value:
            if hasattr(self, "request") and self.request.user.is_authenticated:
                return queryset.filter(author=self.request.user)
            return queryset.none()
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]
