from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.db.models import Prefetch
from apps.user.models import Vendor
from .models import Contract, ContractFile
from .forms import ContractForm
from django.db.models import Q
class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contract_create.html"
    success_url = reverse_lazy("contracts:contract_list")

    def get_initial(self):
        initial = super().get_initial()
        vendor_id = self.request.GET.get("vendor_id")
        if vendor_id:
            try:
                vendor = Vendor.objects.get(id=vendor_id)
                initial["vendor"] = vendor
            except Vendor.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        vendor = form.cleaned_data.get("vendor")
        join_date = form.cleaned_data.get("join_date")
        expiry_date = join_date + timedelta(days=365)

        # Check for existing active contract, excluding expiring contracts
        try:
        
            active_contract = Contract.objects.get(
                vendor=vendor,
                is_active=True,
            )

            if active_contract:
                # If an active contract exists, replace it with the new one
                active_contract.is_active = False
                active_contract.save()
                messages.info(self.request, "An active contract was found and has been replaced with the new one.")
        except Contract.DoesNotExist:
            # No active contract found, proceed with the new contract
            pass

        # Set additional fields before saving
        form.instance.expiry_date = expiry_date
        form.instance.created_by = self.request.user
        messages.success(self.request, "Contract created successfully!")  

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        next_month = today + timedelta(days=30)
        context["expiring_contracts"] = Contract.objects.filter(
            expiry_date__gte=today,  # Expiry date is today or later
            expiry_date__lte=next_month  # Expiry date is within the next 30 days
        )
        return context

class ContractListView(ListView):
    model = Contract
    template_name = "contracts/contract_list.html"
    context_object_name = "contracts"

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Contract.objects.filter(is_active=True).order_by('-created_at')
        if query:
            queryset = queryset.filter(
                Q(vendor__name__icontains=query)
            )
        return queryset
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        next_month = today + timedelta(days=30)
        context["expiring_contracts"] = Contract.objects.filter(
            is_active=True,
            expiry_date__range=(today, next_month)
        )
        return context

class VendorContractManageView(TemplateView):
    template_name = 'contracts/vendor_contract_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_pk = self.kwargs.get('pk')
        contract = get_object_or_404(
            Contract.objects.prefetch_related(
                Prefetch('files', queryset=ContractFile.objects.order_by('-uploaded_at'))
            ),
            pk=contract_pk
        )        


        context['vendor'] = contract.vendor
        context['contract'] = contract
        context['form'] = ContractForm()
        return context

    def post(self, request, *args, **kwargs):
        contract_pk = self.kwargs.get("pk")
        contract = get_object_or_404(Contract, pk=contract_pk)

        action = request.POST.get("action")
        file_id = request.POST.get("file_id")
        vendor = contract.vendor    

        # Update existing file
        if action == "update_file" and file_id:
            contract_file = get_object_or_404(ContractFile, id=file_id)
            new_file = request.FILES.get("file")
            if new_file:
                contract_file.file.delete()  # delete old file from storage
                contract_file.file = new_file
                contract_file.save()
                messages.success(request, "File updated successfully.")
            else:
                messages.error(request, "No file provided for update.")

        # Delete file
        elif action == "delete_file" and file_id:
            contract_file = get_object_or_404(ContractFile, id=file_id)
            contract_file.file.delete()
            contract_file.delete()
            messages.success(request, "File deleted successfully.")

        # Update contract
        elif action == "update_contract" and contract_pk:
            contract = get_object_or_404(Contract, id=contract_pk, vendor=vendor)
            form = ContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                messages.success(request, "Contract updated successfully.")
            else:
                messages.error(request, "Failed to update contract.")


        # Handle file upload for existing contract
        elif action == "add_files" and contract_pk:
            # contract = get_object_or_404(Contract, id=contract_pk, vendor=vendor)
            files = request.FILES.getlist("files")

            if files:
                for file in files:
                    ContractFile.objects.create(
                        contract=contract,
                        file=file,
                        uploaded_by=request.user  
                    )
                messages.success(request, "Files uploaded successfully.")
            else:
                messages.error(request, "No files selected to upload.")

        return redirect(reverse("contracts:vendor_contract_manage", kwargs={"pk": contract_pk}))

    
class VendorContractDeleteView(View):
    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        contract.is_active= False
        contract.save()
        
        messages.success(request, "Contract deleted successfully.")

        return redirect(reverse("contracts:contract_list"))

class ExpiringContractsListView(ListView):
    model = Contract
    template_name = "contracts/expiring_contracts.html"
    context_object_name = "expiring_contracts"

    def get_queryset(self):
        today = now().date()
        next_month = today + timedelta(days=30)
        # Filter contracts expiring within the next 30 days
        return Contract.objects.filter(
            is_active=True,
            expiry_date__gte=today,  # Expiry date is today or later
            expiry_date__lte=next_month  # Expiry date is within the next 30 days
        ).order_by("expiry_date")
    

class InactiveContractsListView(ListView):
    model = Contract
    template_name = "contracts/inactive_contracts.html"
    context_object_name = "inactive_contracts"

    def get_queryset(self):
        return Contract.objects.filter(
           is_active=False,
        ).order_by("vendor__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        next_month = today + timedelta(days=30)
        context["expiring_contracts"] = Contract.objects.filter(
            is_active=True,
            expiry_date__range=(today, next_month)
        )
        return context


@require_GET
def check_active_contract(request):
    vendor_id = request.GET.get('vendor_id')
    has_active = False

    if vendor_id:
        has_active = Contract.objects.filter(
            vendor_id=vendor_id,
            is_active=True,
        ).exists()

    return JsonResponse({'has_active_contract': has_active})