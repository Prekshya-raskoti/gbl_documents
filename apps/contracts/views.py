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

    def post(self, request, *args, **kwargs):
        vendor = request.POST.get('vendor')
        join_date = request.POST.get('join_date')
        expiry_date = request.POST.get('expiry_date')
        terms = request.POST.get('terms')

        if not vendor or not join_date or not expiry_date:
            messages.error(request, "All fields are required.")
            return self.form_invalid(self.get_form())

        created_contracts = []
        counter = 1

        while True:
            file_key = f'file_{counter}' if counter > 1 else 'file'
            contract_file = request.FILES.get(file_key)

            if not contract_file:
                break

            Contract.objects.create(
                vendor_id=vendor,
                join_date=join_date,
                expiry_date=expiry_date,
                file=contract_file,
                created_by=request.user
            )

            created_contracts.append(contract_file)
            counter += 1

        if created_contracts:
            messages.success(request, "Contracts have been successfully uploaded!")
            return redirect(self.success_url)
        else:
            messages.error(request, "Please upload at least one contract file.")
            return self.form_invalid(self.get_form())


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

