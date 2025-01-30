from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class AuthRequireMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            "You are not logged in! Please sign in."
        )
        self.permission_denied_url = reverse_lazy("login")
        return super().dispatch(request, *args, **kwargs)


class NoPermissionHandleMixin:
    permission_denied_message = ""
    permission_denied_url = reverse_lazy("root")

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)


class SuccessMessageDeleteMixin:
    success_message = ""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
