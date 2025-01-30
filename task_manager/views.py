from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'login.html'
    success_message = _('You are logged in')


class LogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
