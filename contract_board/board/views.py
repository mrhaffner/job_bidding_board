from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, request

from contract_board.board.forms import ContractForm, BidForm
from contract_board.board.models import Contract


def contract_list(request):
    if request.method == "POST":
        form = ContractForm(request.post)
    else:  # if its "GET" then create a blank form
        form = ContractForm()
    return render(request, 'contract_list.html', {'form': form})


def contract(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    form = ContractForm(for_contract=contract_)
    # model = Contract.concrete_model(mod_contract=contract_)
    if request.method == 'POST':
        form = ContractForm(for_contract=contract_, data=request.POST)
        form = BidForm(request.post)
    else:

        form = BidForm()

    return render(request, 'contract.html', {'contract': contract_, "form": form})