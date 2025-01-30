from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]


class UserUpdateForm(UserForm):
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(
                username__iexact=username
            ).exists()
            and self.instance.username != username
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username
