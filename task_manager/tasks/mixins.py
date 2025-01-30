from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class CheckTaskCreatorMixin(UserPassesTestMixin):
    def test_func(self):
        task = self.get_object()
        return task.creator == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            "A task can only be deleted by its author"
        )
        self.permission_denied_url = reverse_lazy("tasks:index")
        return super().dispatch(request, *args, **kwargs)
