import django_stubs_ext

from django.contrib.auth.forms import UserCreationForm

from board.models import User

django_stubs_ext.monkeypatch()  # for generics to work


class CustomUserCreationForm(UserCreationForm):
    """A form for creating a contractor/ee user."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'agency_name', 'type')