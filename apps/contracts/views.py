from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta, date


from apps.user.models import Vendor
from .models import Contract
from .forms import ContractForm

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contract_create.html"
    success_url = reverse_lazy("contracts:contract_list")

    def form_valid(self, form):
        vendor = form.cleaned_data.get("vendor")
        join_date = form.cleaned_data.get("join_date")
        expiry_date = join_date + timedelta(days=365)

        # Check for existing active contract
        active_contract = Contract.objects.filter(
            vendor=vendor,
            join_date__lte=now().date(),
            expiry_date__gte=now().date()
        ).exists()

        if active_contract:
            messages.error(self.request, f"{vendor.name} already has an active contract.")
            return redirect("contracts:contract_list")

        form.instance.expiry_date = expiry_date
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        next_week = today + timedelta(days=7)
        context["expiring_contracts"] = Contract.objects.filter(
            expiry_date__range=(today, next_week)
        )
        return context


class ContractListView(ListView):
    model = Contract
    template_name = "contracts/contract_list.html"
    context_object_name = "contracts"

    def get_queryset(self):
        return Contract.objects.all().order_by("-expiry_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        next_week = today + timedelta(days=7)
        context["expiring_contracts"] = Contract.objects.filter(
            expiry_date__range=(today, next_week)
        )
        return context

class VendorContractManageView(TemplateView):
    template_name = 'contracts/vendor_contract_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        # Get the vendor using the pk from the URL
        vendor_pk = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_pk)
        # Get all contracts of the vendor
        context['vendor'] = vendor
        context['vendor_contracts'] = Contract.objects.filter(vendor=vendor).order_by('expiry_date')
        print(context['vendor_contracts'])
        context['form'] = ContractForm()  # Form for adding/updating contracts
        return context

    def post(self, request, *args, **kwargs):
        vendor_pk = self.kwargs.get("pk")
        vendor = get_object_or_404(Vendor, pk=vendor_pk)

        contract_id = request.POST.get("contract_id")
        action = request.POST.get("action")

        # Update contract
        if action == "update":
            contract = get_object_or_404(Contract, id=contract_id, vendor=vendor)
            form = ContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                messages.success(request, "Contract updated successfully.")
            else:
                messages.error(request, "Failed to update contract.")

        #  Delete contract
        elif action == "delete":
            contract = get_object_or_404(Contract, id=contract_id, vendor=vendor)
            contract.delete()
            messages.success(request, "Contract deleted successfully.")

        return redirect(reverse("contracts:vendor_contract_manage", kwargs={"pk": vendor.pk}))
