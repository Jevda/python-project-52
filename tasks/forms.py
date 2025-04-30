# tasks/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Task
# Импорты Status и Label не обязательны здесь, если поля обрабатываются через Meta

# --- Кастомный класс поля для выбора пользователя (остается без изменений) ---
class UserChoiceField(forms.ModelChoiceField):
    """
    Кастомное поле для выбора пользователя, отображающее полное имя.
    """
    def label_from_instance(self, obj):
        # Возвращаем полное имя пользователя
        return obj.get_full_name()

# --- Форма для создания и редактирования Задачи ---
class TaskForm(forms.ModelForm):
    # !!! УБИРАЕМ явное определение поля executor отсюда !!!
    # executor = UserChoiceField(...) # <-- ЭТОЙ СТРОКИ БОЛЬШЕ НЕТ

    class Meta:
        model = Task
        # Список полей остается прежним
        fields = ['name', 'description', 'status', 'executor', 'labels']
        # Метки полей
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }
        # Виджеты полей
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            # !!! Виджет для executor теперь определяется здесь, а не в явном поле !!!
            'executor': forms.Select(attrs={'class': 'form-select'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        # --- НОВОЕ: Указываем Django использовать наш кастомный класс для поля 'executor' ---
        field_classes = {
            'executor': UserChoiceField, # <-- Связываем поле модели 'executor' с классом UserChoiceField
        }