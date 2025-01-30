from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):

    def get_absolute_url(self):
        return reverse('users:index')

    def __str__(self):
        return self.get_full_name()
