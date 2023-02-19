from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from board.forms import ContractForm, BidForm
from board.models import Contract, Bid


@require_http_methods(["GET", "POST"])
def contract_list(request):
    """
    View function for listing contracts and adding new ones.

    GET: renders the contract list page with all existing contracts.
    POST: creates a new contract and saves it to the database if the form is valid.
          otherwise, it displays an error message to the user.

    Args:
        request (HttpRequest): the HTTP request object.

    Returns:
        HttpResponse: the HTTP response object containing the contract list page.

    """
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contract created successfully!')
        else:
            messages.warning(request, 'Error creating bid: {}'.format(form.errors.get_json_data()))
        return redirect(request.path)

    contracts = Contract.objects.all()[::-1]
    form = ContractForm()
    return render(request, 'contract_list.html', {'contracts': contracts, 'form': form})


@require_http_methods(["GET", "POST"])
def contract(request, contract_id):
    """
    View function for displaying the details of a contract and adding new bids.

    GET: renders the contract page with all existing bids.
    POST: creates a new bid and saves it to the database if the form is valid.
          otherwise, it displays an error message to the user.

    Args:
        request (HttpRequest): the HTTP request object.
        contract_id (int): the id of the contract to display.

    Returns:
        HttpResponse: the HTTP response object containing the contract page.

    """
    contract = Contract.objects.get(id=contract_id)

    if request.method == 'POST':
        form = BidForm(for_contract=contract, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bid created successfully!')
        else:
            messages.warning(request, 'Error creating bid: {}'.format(form.errors.get_json_data()))
            return redirect(request.path)

    form = BidForm(for_contract=contract)
    bids = Bid.objects.filter(contract__pk=contract.pk)[::-1]
    return render(request, 'contract.html', {'contract': contract, 'bids': bids, 'form': form})
