# tasks/models.py
# Файл для моделей приложения tasks
# Импортируем стандартную модель пользователя
from django.contrib.auth.models import User
from django.db import models

# Импортируем модель метки из приложения labels
from labels.models import Label

# Импортируем модель статуса из приложения statuses
from statuses.models import Status


# Определяем модель для Задачи
class Task(models.Model):
    # Имя задачи: Обязательное текстовое поле
    name = models.CharField(
        max_length=150,
        unique=True,  # Имя задачи должно быть уникальным
        blank=False,
        null=False,
        verbose_name="Имя",
    )
    # Описание задачи: Большое текстовое поле, не обязательное
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    # Статус задачи: Связь с моделью Status (один-ко-многим)
    # Обязательное поле.
    # on_delete=models.PROTECT: Запрещает удаление статуса, если с ним связана
    # хотя бы одна задача.
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=False,  # Статус обязателен
        blank=False,
        verbose_name="Статус",
        related_name="tasks",  # Имя для обратной связи от Status к Task
    )
    # Автор задачи: Связь с моделью User (один-ко-многим)
    # Обязательное поле. Устанавливается автоматически при создании.
    # on_delete=models.PROTECT: Запрещает удаление пользователя (автора),
    # если у него есть задачи.
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,  # Автор обязателен
        blank=False,
        verbose_name="Автор",
        related_name="authored_tasks",  # Имя для обратной связи от User к Task
    )
    # Исполнитель задачи: Связь с моделью User (один-ко-многим)
    # Не обязательное поле (задачу можно создать без исполнителя).
    # on_delete=models.PROTECT: Запрещает удаление пользователя (исполнителя),
    # если на него назначены задачи.
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,  # Исполнитель не обязателен
        blank=True,
        verbose_name="Исполнитель",
        related_name="executed_tasks",  # Имя для обратной связи от User к Task
    )
    # Дата создания: Заполняется автоматически при создании
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    # Связь с Метками (многие-ко-многим)
    labels = models.ManyToManyField(
        Label,
        blank=True,  # Можно не указывать метки
        verbose_name="Метки",
        related_name="tasks",
    )

    # Метод __str__ для строкового представления задачи
    def __str__(self):
        return self.name

    # Класс Meta для настроек модели
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]  # Сортировка: новые задачи сверху
