# statuses/forms.py
# Файл для форм приложения statuses

from django import forms

from .models import Status  # Импортируем нашу модель Status


# Создаем форму на основе модели Status
class StatusForm(forms.ModelForm):
    class Meta:
        # Указываем модель, с которой связана форма
        model = Status
        # Указываем поля модели, которые должны быть в форме
        # Нам нужно только поле 'name'
        fields = ["name"]
        # Задаем метку для поля 'name'
        labels = {
            "name": "Имя",
        }
