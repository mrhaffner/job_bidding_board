from django import forms

from board.models import Bid, Contract

DUPLICATE_ITEM_ERROR = "You've already got this in your list"
EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['contract_title',
                  'agency_name',
                  'contact_information',
                  'bidding_end_date',
                  'job_description']

    def clean(self):
        cleaned_data = super().clean()
        contract_title = cleaned_data.get('contract_title')
        existing_contracts = Contract.objects.filter(contract_title=contract_title)
        if self.instance.pk:
            existing_contracts = existing_contracts.exclude(pk=self.instance.pk)
        if existing_contracts.exists():
            raise forms.ValidationError('This contract title already exists')
        if not contract_title:
            raise forms.ValidationError(EMPTY_ITEM_ERROR)
        return cleaned_data


class BidForm(forms.ModelForm):

    def __init__(self, for_contract, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.contract = for_contract

    class Meta:
        model = Bid
        fields = ['contractor_name', 'amount', 'contact_information']
