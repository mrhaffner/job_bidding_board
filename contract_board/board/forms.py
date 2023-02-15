from django.forms import ModelForm

from board.models import Bid, Contract


class ContractForm(ModelForm):

    class Meta:
        model = Contract
        fields = ['contract_title',
                  'agency_name',
                  'contact_information',
                  'bidding_end_date',
                  'job_description']


class BidForm(ModelForm):

    def __init__(self, for_contract, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.contract = for_contract

    class Meta:
        model = Bid
        fields = ['contractor_name', 'amount', 'contact_information']