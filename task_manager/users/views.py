from django.contrib import messages
from django.contrib.auth import get_user_model
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
from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.users.mixins import CheckSelfUserMixin


class IndexView(ListView):
    model = get_user_model()
    template_name = "users/index.html"
    fields = ["first_name", "last_name", "username", "password1", "password2"]


class UserCreate(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = "users/create.html"
    success_message = _("User successfully registered")
    success_url = reverse_lazy("login")


class UserUpdate(
    NoPermissionHandleMixin,
    AuthRequireMixin,
    CheckSelfUserMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_message = _("User successfully updated")


class UserDelete(
    NoPermissionHandleMixin,
    AuthRequireMixin,
    CheckSelfUserMixin,
    SuccessMessageDeleteMixin,
    DeleteView,
):
    model = get_user_model()
    success_url = reverse_lazy("users:index")
    success_message = _("User successfully deleted")
    template_name = "users/delete.html"

    def post(self, request, *args, **kwargs):
        if (
            self.get_object().creator.all().exists()
            or self.get_object().executor.all().exists()
        ):
            messages.error(
                self.request, _("Unable to delete user because it is in use")
            )
            return redirect("users:index")

        return super().post(request, *args, **kwargs)
