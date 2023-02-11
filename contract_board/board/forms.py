from django import forms

class BidForm(forms.Form):
    contractor_name = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    contact_information = forms.CharField(widget=forms.Textarea)

class ContractForm(forms.Form):
    contract_title = forms.CharField(max_length=100)
    agency_name = forms.CharField(max_length=100)
    contact_information = forms.CharField(widget=forms.Textarea)
    bidding_end_date = forms.DateField()
    job_description = forms.CharField(widget=forms.Textarea)