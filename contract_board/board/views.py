from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from board.forms import ContractForm, BidForm
from board.models import Contract, Bid


@require_http_methods(["GET", "POST"])
def contract_list(request):
    """
    Handles GET and Post request
    Post will add information from the ContractForm and renders the contract_list.html page
    GET will render the contract_list.html page, passing in a list of all the Contract models as 'contracts'
    """
    if request.method == "POST":
        form = ContractForm(request.POST)
        form.save()
        return redirect(request.path)

    contracts = Contract.objects.all()[::-1]
    form = ContractForm()
    return render(request, 'contract_list.html', {'contracts': contracts, 'form': form})


@require_http_methods(["GET", "POST"])
def contract(request, contract_id):
    """
    handles a GET and POST request
    POST will add information from the BidForm and render the contract.html page
    (contract_id does not come from the form when creating the new Bid)
    GET will render the contract.html page, passing in Contract model corresponding
    to the contract_id as 'contract'
    """
    contract = Contract.objects.get(id=contract_id)

    if request.method == 'POST':
        form = BidForm(for_contract=contract, data=request.POST)
        form.save()
        return redirect(request.path)

    form = BidForm(for_contract=contract)
    bids = Bid.objects.filter(contract__pk=contract.pk)[::-1]
    return render(request, 'contract.html', {'contract': contract, 'bids': bids, 'form': form})