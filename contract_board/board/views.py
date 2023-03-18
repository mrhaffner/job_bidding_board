from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from board.forms import CustomUserCreationForm
from board.models import Bid, Contract


class ContractListView(LoginRequiredMixin, ListView):
    """
    A view that lists all contracts.
    A user must be authenticated to see this view.
    """
    model = Contract


class ContractCreateView(LoginRequiredMixin, CreateView):
    """
    A view that allows a user to create a contract.
    A user must be authenticated to see/use this view.
    """
    model = Contract
    fields = ['contract_title', 'bidding_end_date', 'job_description']
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.contractee = self.request.user
        return super().form_valid(form)


class ContractDetailView(LoginRequiredMixin, DetailView):
    """
    A view that allows a user to view a contract.
    A user must be authenticated to see this view.
    """
    model = Contract


class BidCreateView(LoginRequiredMixin, CreateView):
    """
    A view that allows a user to create a bid.
    A user must be authenticated to see/use this view.
    """
    model = Bid
    fields = ['amount']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.contractor = self.request.user
        form.instance.contract = Contract.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self) -> any:
        return reverse_lazy('contract_view', kwargs={'pk': self.kwargs['pk']})


class UserCreateView(CreateView):
    """
    A view that allows a user to create an account.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class UserView(LoginRequiredMixin, TemplateView):
    """
    A view that allows a user to view their user details and any bids/contracts they have created.
    A user must be authenticated to see this view.
    """
    template_name = 'user/user.html'

    def get_context_data(self, *args, **kwargs) -> dict[str, any]:  # noqa: ANN002, ANN003
        context = super(UserView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        if user.type == 'CONTRACTEE':
            contracts = Contract.objects.filter(contractee=user)
        else:
            contracts = Contract.objects.filter(bid__contractor=user).distinct()

        context.update({
            'user': self.request.user,
            'contracts': contracts
        })
        return context