import django_stubs_ext

from django.forms import ModelForm

from board.models import Bid, Contract

django_stubs_ext.monkeypatch()  # for generics to work


class ContractForm(ModelForm[Contract]):

    class Meta:
        model = Contract
        fields = ['contract_title',
                  'agency_name',
                  'contact_information',
                  'bidding_end_date',
                  'job_description']


class BidForm(ModelForm[Bid]):

    def __init__(self, for_contract: Contract, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self.instance.contract = for_contract

    class Meta:
        model = Bid
        fields = ['contractor_name', 'amount', 'contact_information']