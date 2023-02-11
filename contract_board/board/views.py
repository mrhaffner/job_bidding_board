from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from board.forms import ContractForm, BidForm
from board.models import Contract, Bid


@require_http_methods(["GET", "POST"])
def contract_list(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        print(form.data)
        if form.is_valid():
            form.save()
        return redirect(request.path)

    contracts = Contract.objects.all()
    form = ContractForm() # sort?
    return render(request, 'contract_list.html', {'contract': contracts, 'form': form})


@require_http_methods(["GET", "POST"])
def contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)

    if request.method == 'POST':
        form = BidForm(for_contract=contract, data=request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

    form = BidForm(for_contract=contract)
    bids = Bid.objects.filter(contract__pk=contract.pk) # sort?
    return render(request, 'contract.html', {'contract': contract,  'bids': bids, 'form': form})