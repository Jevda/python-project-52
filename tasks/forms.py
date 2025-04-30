# tasks/forms.py
from django import forms
from django.contrib.auth.models import User

from .models import Task


# --- Определение UserChoiceField (здесь, один раз) ---
class UserChoiceField(forms.ModelChoiceField):
    """Кастомное поле для выбора пользователя, отображающее полное имя.
    """

    def label_from_instance(self, obj):
        # !!! Добавляем print для финальной проверки, если хотите !!!
        # E501 fix: wrapped line
        # print(
        #     f"--- DEBUG [forms.py]: label_from_instance для {obj.username},"
        #     f" вернул '{obj.get_full_name()}'"
        # )
        return obj.get_full_name()


# --- Форма для создания и редактирования Задачи ---
class TaskForm(forms.ModelForm):
    # --- Явное определение поля executor с ЯВНОЙ меткой ---
    executor = UserChoiceField(
        queryset=User.objects.all(),
        required=False,
        # E261 fix: added spaces
        label="Исполнитель",  # !!! Явная метка !!!
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            # 'executor': 'Исполнитель', # Убрали, т.к. label задан выше
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # E501 fix: wrapped line
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3},
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            # E501 fix: wrapped comment
            # 'executor': forms.Select(attrs={'class': 'form-select'}),
            # # Убрали, т.к. widget задан выше
            "labels": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
