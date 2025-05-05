from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_("Status"),
        related_name="tasks",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_("Author"),
        related_name="authored_tasks",
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Executor"),
        related_name="executed_tasks",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date"),
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_("Labels"),
        related_name="tasks",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ["-created_at"]
