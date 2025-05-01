# users/views.py
# Файл для представлений (views) приложения users

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Добавляем DeleteView и миксины
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm


# Класс для отображения списка пользователей
class UsersIndexView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"


# Класс для регистрации нового пользователя
class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "users/create.html"
    success_message = "Пользователь успешно зарегистрирован"

    def get_success_url(self):
        return reverse_lazy("login")


# Класс для входа пользователя
class UserLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


# Класс для выхода пользователя
class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


# Класс для редактирования пользователя
class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:index")
    success_message = "Пользователь успешно изменен"

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users:index")


# --- Новое представление для удаления пользователя ---
class UserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = User  # Работаем с моделью User
    template_name = "users/delete.html"  # Шаблон подтверждения удаления
    success_url = reverse_lazy("users:index")  # Куда перенаправить после успеха
    success_message = "Пользователь успешно удален"  # Сообщение об успехе

    # Проверка прав: пользователь может удалить только себя
    def test_func(self):
        return self.get_object() == self.request.user

    # Обработка отказа в доступе
    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users:index")

    # TODO: Позже добавить сюда проверку, связан ли пользователь с задачами
    # def post(self, request, *args, **kwargs):
    #     user_to_delete = self.get_object()
    #     if user_has_related_tasks(user_to_delete): # Условная функция проверки
    #         messages.error(
    #             request,
    #             "Невозможно удалить пользователя, потому что он связан"
    #             " с задачами"
    #         )
    #         return redirect('users:index')
    #     # Если проверки пройдены, вызываем стандартный метод удаления
    #     messages.success(self.request, self.success_message)
    #     # Добавляем сообщение вручную, т.к. SuccessMessageMixin может не
    #     # сработать при переопределении post/delete
    #     return super().delete(request, *args, **kwargs)
    #     # Используем delete, а не post