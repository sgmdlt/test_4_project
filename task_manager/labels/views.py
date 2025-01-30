from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import (
    AuthRequireMixin,
    NoPermissionHandleMixin,
    SuccessMessageDeleteMixin,
)


class IndexView(NoPermissionHandleMixin, AuthRequireMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class LabelCreate(
    NoPermissionHandleMixin, AuthRequireMixin, SuccessMessageMixin, CreateView
):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_message = _("Label successfully created")


class LabelUpdate(
    NoPermissionHandleMixin, AuthRequireMixin, SuccessMessageMixin, UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_message = _("Label successfully updated")


class LabelDelete(
    NoPermissionHandleMixin,
    AuthRequireMixin,
    SuccessMessageDeleteMixin,
    DeleteView,
):
    model = Label
    success_url = reverse_lazy("labels:index")
    success_message = _("Label successfully deleted")
    template_name = "labels/delete.html"

    def post(self, request, *args, **kwargs):
        if self.get_object().labels.all().exists():
            messages.error(
                self.request, _("Unable to delete label because it is in use")
            )
            return redirect("labels:index")

        return super().post(request, *args, **kwargs)
