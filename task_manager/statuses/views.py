from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    AuthRequireMixin,
    NoPermissionHandleMixin,
    SuccessMessageDeleteMixin,
)
from task_manager.statuses.forms import TaskStatusForm
from task_manager.statuses.models import TaskStatus


class IndexView(NoPermissionHandleMixin, AuthRequireMixin, ListView):
    model = TaskStatus
    template_name = "statuses/index.html"


class TaskStatusCreate(
    NoPermissionHandleMixin, AuthRequireMixin, SuccessMessageMixin, CreateView
):
    model = TaskStatus
    form_class = TaskStatusForm
    template_name = "statuses/create.html"
    success_message = _("Status successfully created")


class TaskStatusUpdate(
    NoPermissionHandleMixin, AuthRequireMixin, SuccessMessageMixin, UpdateView
):
    model = TaskStatus
    form_class = TaskStatusForm
    template_name = "statuses/update.html"
    success_message = _("Status successfully updated")


class TaskStatusDelete(
    NoPermissionHandleMixin,
    AuthRequireMixin,
    SuccessMessageDeleteMixin,
    DeleteView,
):
    model = TaskStatus
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully deleted")
    template_name = "statuses/delete.html"

    def post(self, request, *args, **kwargs):
        if self.get_object().status.all().exists():
            messages.error(
                self.request, _("Unable to delete status because it is in use")
            )
            return redirect("statuses:index")

        return super().post(request, *args, **kwargs)
