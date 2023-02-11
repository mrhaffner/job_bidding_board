from django.forms import ModelForm

from board.models import Bid, Contract


class ContractForm(ModelForm):

    class Meta:
        model = Contract
        fields = ['contract_title', 'agency_name', 'contact_information', 'bidding_end_date', 'job_description']


class BidForm(ModelForm):

    class Meta:
        model = Bid
        fields = ['contractor_name', 'amount', 'contact_information']

# labels
# class BidForm(forms.Form):
#     contractor_name = forms.CharField(max_length=100) # differs from model
#     amount = forms.DecimalField(max_digits=10, decimal_places=2) # differs from model
#     contact_information = forms.CharField(widget=forms.Textarea)


# class ContractForm(forms.Form):
#     contract_title = forms.CharField(max_length=100) # differs from model
#     agency_name = forms.CharField(max_length=100) # differs from model
#     contact_information = forms.CharField(widget=forms.Textarea) # differs from model, text area???
#     bidding_end_date = forms.DateField()
#     job_description = forms.CharField(widget=forms.Textarea) # differs from model

