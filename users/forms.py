# users/forms.py
# Файл для форм приложения users

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Форма регистрации (остается без изменений)
class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }


# --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
# Форма для редактирования пользователя
class UserUpdateForm(forms.ModelForm):
    # Явно добавляем поля для пароля, делаем их НЕ обязательными
    # Используем имена password1 и password2, чтобы ID были
    # id_password1 и id_password2
    password1 = forms.CharField(  # <--- Переименовано с 'password'
        label="Пароль",
        required=False,
        widget=forms.PasswordInput,
        help_text="Оставьте пустым, если не хотите менять пароль.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=False,
        widget=forms.PasswordInput,
        help_text="Повторите пароль, если меняете его.",
    )

    class Meta:
        model = User
        # В Meta указываем только поля профиля (без паролей)
        fields = ("first_name", "last_name", "username")
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }

    # Проверяем, что если пользователь ввел пароль, то оба поля совпадают
    def clean_password2(self):
        # Получаем значения из password1 и password2
        password1 = self.cleaned_data.get("password1")
        # <--- Изменено с 'password'
        password2 = self.cleaned_data.get("password2")
        # Проверяем только если оба поля чем-то заполнены
        if password1 and password2 and password1 != password2:
            # <--- Изменено с 'password'
            raise forms.ValidationError("Пароли не совпадают.")
        # Этот метод ОБЯЗАТЕЛЬНО должен вернуть значение второго пароля
        return password2

    # Переопределяем метод сохранения
    def save(self, commit=True):
        # Сначала получаем объект пользователя из стандартного
        # сохранения ModelForm
        user = super().save(commit=False)
        # Получаем пароль из очищенных данных формы password1
        password = self.cleaned_data.get("password1")
        # <--- Изменено с 'password'
        # Если пользователь ввел что-то в поле пароля
        if password:
            # Устанавливаем пароль с использованием set_password для хеширования
            user.set_password(password)
        # Если нам нужно сохранить объект в БД
        if commit:
            user.save()
        # Возвращаем сохраненный объект пользователя
        return user
# --- КОНЕЦ ИЗМЕНЕНИЙ ---