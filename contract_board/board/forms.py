import django_stubs_ext

from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from board.models import Bid, Contract, User

django_stubs_ext.monkeypatch()  # for generics to work


class ContractForm(ModelForm[Contract]):
    """A form for creating a contract."""

    class Meta:
        model = Contract
        fields = ['contract_title', 'bidding_end_date', 'job_description']


class BidForm(ModelForm[Bid]):
    """A form for creating a bid."""

    def __init__(self, for_contract: Contract, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self.instance.contract = for_contract

    class Meta:
        model = Bid
        fields = ['amount']


class CustomUserCreationForm(UserCreationForm):
    """A form for creating a contractor/ee user."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'agency_name', 'type')