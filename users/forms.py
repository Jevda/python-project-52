# users/forms.py
"""Forms for the users application."""

from typing import Any, ClassVar

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Сообщение об ошибке вынесем в константу
PASSWORD_MISMATCH_ERROR = "Пароли не совпадают."


# Форма регистрации (остается без изменений)
class UserRegisterForm(UserCreationForm):
    """Form for user registration."""

    class Meta(UserCreationForm.Meta):
        """Metadata options for the UserRegisterForm."""

        model = User
        fields = ("first_name", "last_name", "username")
        labels: ClassVar[dict[str, str]] = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }


# Форма для редактирования пользователя
class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile information, including password change."""

    # Явно добавляем поля для пароля, делаем их НЕ обязательными
    # Используем имена password и password2 (как в UserCreationForm)
    password = forms.CharField(
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
        """Metadata options for the UserUpdateForm."""

        model = User
        # В Meta указываем только поля профиля (без паролей)
        fields = ("first_name", "last_name", "username")
        labels: ClassVar[dict[str, str]] = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }

    def clean_password2(self) -> str | None:
        """Validate that the two password fields match."""
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        # Проверяем только если оба поля чем-то заполнены
        if password and password2 and password != password2:
            # Используем константу для сообщения об ошибке (EM101, TRY003 fix)
            raise forms.ValidationError(PASSWORD_MISMATCH_ERROR)
        # Этот метод ОБЯЗАТЕЛЬНО должен вернуть значение второго пароля
        return password2

    # commit сделан keyword-only (FBT002 fix)
    def save(self, *, commit: bool = True) -> User:
        """Save the provided password in hashed format if it exists."""
        # Сначала получаем объект пользователя из стандартного сохранения ModelForm
        user = super().save(commit=False)
        # Получаем пароль из очищенных данных формы password
        password = self.cleaned_data.get("password")
        # Если пользователь ввел что-то в поле пароля
        if password:
            # Устанавливаем пароль с использованием set_password для хеширования
            user.set_password(password)
        # Если нам нужно сохранить объект в БД
        if commit:
            user.save()
        # Возвращаем сохраненный объект пользователя
        return user