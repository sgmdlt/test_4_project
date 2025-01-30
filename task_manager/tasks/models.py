from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import TaskStatus


class Task(models.Model):
    name = models.CharField(_('name'), max_length=150, unique=True)
    description = models.TextField(_('description'), blank=True)
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('status'),
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='creator',
        verbose_name=_('creator'),
    )
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        blank=True,
        null=True,
        verbose_name=_('executor'),
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabels',
        related_name='labels',
        blank=True,
        verbose_name=_('labels'),
    )
    created_at = models.DateTimeField(_('created date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('tasks:index')

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
