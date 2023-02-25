from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect, \
    HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, FormView, View
from django.views.generic.detail import SingleObjectMixin

from board.forms import ContractForm, BidForm, CustomUserCreationForm
from board.models import Contract, Bid


class ContractListView(LoginRequiredMixin, ListView):
    """"""
    model = Contract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContractForm()
        return context


class ContractFormView(SingleObjectMixin, FormView):
    """"""
    template_name = 'board/contract_list.html'
    form_class = ContractForm
    success_url = reverse_lazy('home')


class ContractBoardView(View):
    """"""
    def get(self, request, *args, **kwargs):
        view = ContractListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ContractFormView.as_view()
        return view(request, *args, **kwargs)


@require_http_methods(["GET", "POST"])
def contract_list(request: HttpRequest
                  ) -> (HttpResponseRedirect
                        | HttpResponsePermanentRedirect
                        | HttpResponse):
    """
    Handles GET and Post request
    Post will add information from the ContractForm and renders the contract_list.html page
    GET will render the contract_list.html page, passing in a list of all the Contract models as
    'contracts'
    """
    if request.method == "POST":
        form = ContractForm(request.POST)
        form.save()
        return redirect(request.path)

    contracts = Contract.objects.all()[::-1]
    form = ContractForm()
    return render(request, 'contract_list.html', {'contracts': contracts, 'form': form})


@require_http_methods(["GET", "POST"])
def contract(request: HttpRequest,
             contract_id: str
             ) -> (HttpResponseRedirect
                   | HttpResponsePermanentRedirect
                   | HttpResponse):
    """
    Handles a GET and POST request
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


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # correct?
    template_name = 'registration/register.html'