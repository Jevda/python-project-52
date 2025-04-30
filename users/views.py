# users/views.py
"""Views for the users application."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm


# Класс для отображения списка пользователей
class UsersIndexView(ListView):
    """View to display a list of all registered users."""

    model = User
    template_name = "users/index.html"
    context_object_name = "users"


# Класс для регистрации нового пользователя
class UserRegisterView(SuccessMessageMixin, CreateView):
    """View for new user registration."""

    form_class = UserRegisterForm
    template_name = "users/create.html"
    success_message = "Пользователь успешно зарегистрирован"

    def get_success_url(self) -> str:
        """Return the URL to redirect to after successful registration."""
        return reverse_lazy("login")


# Класс для входа пользователя
class UserLoginView(LoginView):
    """View for user login."""

    template_name = "users/login.html"

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        """Add a success message upon successful login."""
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


# Класс для выхода пользователя
class UserLogoutView(LogoutView):
    """View for user logout."""

    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponseRedirect | HttpResponse:
        """Add a success message upon successful logout."""
        if request.user.is_authenticated:
            messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


# Класс для редактирования пользователя (E501 fix: перенос строки)
class UserUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """View for updating a user's own profile."""

    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:index")
    success_message = "Пользователь успешно изменен"

    def test_func(self) -> bool:
        """Check if the logged-in user matches the user being updated."""
        return self.get_object() == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        """Handle unauthorized access attempt."""
        # E501 fix: перенос строки
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя.",
        )
        return redirect("users:index")


# --- Новое представление для удаления пользователя --- (E501 fix: перенос)
class UserDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """View for deleting a user's own profile."""

    model = User  # Работаем с моделью User
    template_name = "users/delete.html"  # Шаблон подтверждения удаления
    success_url = reverse_lazy("users:index")  # Куда перенаправить после успеха
    success_message = "Пользователь успешно удален"  # Сообщение об успехе

    # Проверка прав: пользователь может удалить только себя
    def test_func(self) -> bool:
        """Check if the logged-in user matches the user being deleted."""
        return self.get_object() == self.request.user

    # Обработка отказа в доступе
    def handle_no_permission(self) -> HttpResponseRedirect:
        """Handle unauthorized access attempt."""
        # E501 fix: перенос строки
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя.",
        )
        return redirect("users:index")

    # TODO: Позже добавить сюда проверку, связан ли пользователь с задачами # noqa: TD002, TD003, FIX002