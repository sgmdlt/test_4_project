from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import (
    AuthRequireMixin,
    NoPermissionHandleMixin,
    SuccessMessageDeleteMixin,
)
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.mixins import CheckTaskCreatorMixin
from task_manager.tasks.models import Task


class IndexView(NoPermissionHandleMixin, AuthRequireMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    filterset_class = TaskFilter


class TaskCreate(
    NoPermissionHandleMixin, AuthRequireMixin, SuccessMessageMixin, CreateView
):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdate(
    NoPermissionHandleMixin, AuthRequireMixin, SuccessMessageMixin, UpdateView
):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_message = _("Task successfully updated")


class TaskDelete(
    NoPermissionHandleMixin,
    AuthRequireMixin,
    CheckTaskCreatorMixin,
    SuccessMessageDeleteMixin,
    DeleteView,
):
    model = Task
    success_url = reverse_lazy("tasks:index")
    success_message = _("Task successfully deleted")
    template_name = "tasks/delete.html"


class TaskDetail(NoPermissionHandleMixin, AuthRequireMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
