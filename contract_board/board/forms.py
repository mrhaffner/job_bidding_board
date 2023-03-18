from django.contrib.auth.forms import UserCreationForm

from board.models import User


class CustomUserCreationForm(UserCreationForm):
    """A form for creating a contractor/ee user."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'agency_name', 'type')