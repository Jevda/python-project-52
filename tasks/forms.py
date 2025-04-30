# tasks/forms.py
from django import forms
from .models import Task
# Импортируем модель User, чтобы использовать ее в lambda-функции
from django.contrib.auth.models import User
# Импортируем модель Status для поля статуса
from statuses.models import Status
# Импортируем модель Label для поля меток
from labels.models import Label

class TaskForm(forms.ModelForm):

    # --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
    # Определяем поле executor явно, чтобы настроить отображение
    executor = forms.ModelChoiceField(
        # Указываем queryset как обычно
        queryset=User.objects.all(),
        # Делаем поле необязательным, как в модели
        required=False,
        # Метка поля
        label='Исполнитель',
        # !!! Используем lambda-функцию для label_from_instance !!!
        # Эта функция будет вызываться для каждого пользователя (user) в queryset
        # и возвращать строку, которая будет текстом <option> в select'е.
        # Мы возвращаем полное имя пользователя.
        label_from_instance=lambda user: user.get_full_name()
    )
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    class Meta:
        model = Task
        # Поле executor уже определено выше, поэтому его можно убрать из fields здесь,
        # но оставим для ясности или на случай других настроек Meta.
        # Главное, что явное определение выше переопределит настройки из Meta.
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель', # Эта метка может быть переопределена явным полем выше
            'labels': 'Метки',
        }
        widgets = {
            # Используем SelectMultiple для поля labels (многие-ко-многим)
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
            # Можно добавить виджеты и для других полей при необходимости
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            # 'executor': forms.Select(attrs={'class': 'form-select'}), # Это переопределяется явным полем
        }
