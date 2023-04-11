from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, TemplateView

from board.forms import CustomUserCreationForm
from board.models import Bid, Contract


class ContractListView(LoginRequiredMixin, TemplateView):
    """
    A view that lists all contracts.
    A user must be authenticated to see this view.
    Filters on the bidding end date.
    """
    template_name = 'board/contract_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        today = timezone.now().date()

        if status == 'expired':
            contracts = Contract.objects.filter(bidding_end_date__lt=today)
        elif status == 'all':
            contracts = Contract.objects.all()
        else:
            contracts = Contract.objects.filter(bidding_end_date__gte=today)

        context.update({
            'object_list': contracts
        })
        return context

class ContractCreateView(LoginRequiredMixin, CreateView):
    """
    A view that allows a user to create a contract.
    A user must be authenticated to see/use this view.
    """
    model = Contract
    fields = ['contract_title', 'bidding_end_date', 'job_description']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
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

    def form_valid(self, form):
        form.instance.contractor = self.request.user
        form.instance.contract = Contract.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contract_view', kwargs={'pk': self.kwargs['pk']})


class UserCreateView(CreateView):
    """
    A view that allows a user to create an account.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserView(LoginRequiredMixin, TemplateView):
    """
    A view that allows a user to view their user details and any bids/contracts they have created.
    A user must be authenticated to see this view.
    """
    template_name = 'user/user.html'

    def get_context_data(self, *args, **kwargs):
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