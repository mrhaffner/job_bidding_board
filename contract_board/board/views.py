from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from board.forms import CustomUserCreationForm
from board.models import Contract, Bid


class ContractListView(LoginRequiredMixin, ListView):
    """"""
    model = Contract


class ContractCreateView(LoginRequiredMixin, CreateView):
    """"""
    model = Contract
    fields = ['contract_title', 'bidding_end_date', 'job_description']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.contractee = self.request.user
        return super().form_valid(form)


class ContractDetailView(LoginRequiredMixin, DetailView):
    model = Contract


class BidCreateView(LoginRequiredMixin, CreateView):
    model = Bid
    fields = ['amount']

    def form_valid(self, form):
        form.instance.contractor = self.request.user
        form.instance.contract = Contract.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('contract_view', kwargs={'pk': self.kwargs['pk']})


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # correct?
    template_name = 'registration/register.html'