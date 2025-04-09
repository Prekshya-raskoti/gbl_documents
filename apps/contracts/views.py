from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from .models import Contract
from .forms import ContractForm


def contract_list(request):
    now = timezone.now()

    # Get all contracts
    contracts = Contract.objects.all()

    # Filter those that expire in the next 7 days
    expiring_contracts = contracts.filter(
        expiry_date__lte=now + timedelta(days=7),
        expiry_date__gt=now
    )
    

    return render(request, 'contracts/contract_list.html', {
        'contracts': contracts,
        'expiring_contracts': expiring_contracts
    })

class ContractDetailView(DetailView):
    model = Contract
    template_name = 'contracts/contract_detail.html'
    context_object_name = 'contract'

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contracts:contract_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Contract has been successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with the form submission.")
        return super().form_invalid(form)

class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/edit_contract.html'
    success_url = reverse_lazy('contracts:contract_list')

    def form_valid(self, form):
        messages.success(self.request, "Contract updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating contract.")
        return super().form_invalid(form)

class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'contracts/contract_confirm_delete.html'
    success_url = reverse_lazy('contracts:contract_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Contract deleted successfully.")
        return super().delete(request, *args, **kwargs)

