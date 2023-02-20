import json
import os

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from board.forms import ContractForm, BidForm
from board.models import Contract, Bid


@require_http_methods(["GET", "POST"])
def contract_list(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        form.save()
        return redirect(request.path)

    contracts = Contract.objects.all()[::-1]
    form = ContractForm()
    return render(request, 'contract_list.html', {'contracts': contracts, 'form': form})


@require_http_methods(["GET", "POST"])
def contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)

    if request.method == 'POST':
        form = BidForm(for_contract=contract, data=request.POST)
        form.save()
        return redirect(request.path)

    form = BidForm(for_contract=contract)
    bids = Bid.objects.filter(contract__pk=contract.pk)[::-1]
    return render(request, 'contract.html', {'contract': contract, 'bids': bids, 'form': form})


@csrf_exempt
@require_http_methods(["POST"])
def build(request):
    payload = json.loads(request.body.decode("utf-8"))
    print(payload)
    SECRET_KEY = os.getenv('SECRET_KEY')
    os.system('sh ../scripts/test.sh')
    print("hi")
