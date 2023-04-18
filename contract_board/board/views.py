from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View

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

    def form_valid(self, form):
        form.instance.contractee = self.request.user
        return super().form_valid(form)


class ContractDetailView(LoginRequiredMixin, DetailView):
    """
    A view that allows a user to view a contract.
    A user must be authenticated to see this view.
    """
    model = Contract


class ContractDeleteView(LoginRequiredMixin, View):
    """
    This view is used to delete a contract
    a user must be authinticated to delete a contract
    """
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        contract = get_object_or_404(Contract, pk=id)
        contract.delete()
        return JsonResponse({'success': True})


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


class BidDeleteView(LoginRequiredMixin, View):
    """
    This view is used to delete a bid
    A user must be authenticated to delete a bid
    """
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        bid = get_object_or_404(Bid, pk=id)
        bid.delete()
        return JsonResponse({'success': True})


class BidAcceptView(LoginRequiredMixin, View):
    """
    This view is used to accept a bid.  This also marks the bid's contract as closed.
    A user must be authenticated to accept a bid
    """
    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        bid = get_object_or_404(Bid, pk=id)
        bid.accepted = True
        bid.save()
        contract = bid.contract
        contract.closed = True
        contract.save()
        return JsonResponse({'success': True})


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

        now = timezone.now()
        active_contracts = contracts.filter(bidding_end_date__gte=now, closed=False)
        expired_contracts = contracts.filter(bidding_end_date__lt=now, closed=False)
        closed_contracts = contracts.exclude(closed=False)

        context.update({
            'user': self.request.user,
            'active_contracts': active_contracts,
            'expired_contracts': expired_contracts,
            'closed_contracts': closed_contracts,
        })
        return context