# users/forms.py
# Файл для форм приложения users

from django.contrib.auth.forms import UserCreationForm # Убираем UserChangeForm
from django.contrib.auth.models import User
from django import forms

# Форма регистрации (остается без изменений)
class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username',)
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }

# --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
# Форма для редактирования пользователя
# Наследуемся от ModelForm
class UserUpdateForm(forms.ModelForm):
    # Явно добавляем поля для пароля, делаем их НЕ обязательными
    # Используем PasswordInput для скрытия ввода
    password = forms.CharField(
        label="Пароль",
        required=False, # Не обязательно менять пароль при редактировании профиля
        widget=forms.PasswordInput,
        help_text="Оставьте пустым, если не хотите менять пароль."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=False,
        widget=forms.PasswordInput,
        help_text="Повторите пароль, если меняете его."
    )

    class Meta:
        model = User
        # В Meta указываем только поля профиля
        fields = ('first_name', 'last_name', 'username',)
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }

    # Проверяем, что если пользователь ввел пароль, то оба поля совпадают
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        # Проверяем только если оба поля чем-то заполнены
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        # Этот метод ОБЯЗАТЕЛЬНО должен вернуть значение второго пароля
        return password2

    # Переопределяем метод сохранения
    def save(self, commit=True):
        # Сначала получаем объект пользователя из стандартного сохранения ModelForm,
        # но пока не сохраняем его в БД (commit=False)
        user = super().save(commit=False)
        # Получаем пароль из очищенных данных формы
        password = self.cleaned_data.get("password")
        # Если пользователь ввел что-то в поле пароля
        if password:
            # Устанавливаем пароль с использованием set_password для хеширования
            user.set_password(password)
        # Если нам нужно сохранить объект в БД (обычно commit=True)
        if commit:
            user.save()
        # Возвращаем сохраненный объект пользователя
        return user
