from django.urls import path
from .views import (
    ContractCreateView,
    ContractListView,
    VendorContractManageView,
    VendorContractDeleteView,
    ExpiringContractsListView,
    check_active_contract,
)

app_name = 'contracts'  # Optional: for namespacing URL names

urlpatterns = [
    path('create/', ContractCreateView.as_view(), name='contract_create'),
    path('list/', ContractListView.as_view(), name='contract_list'),
    path('vendor/<int:pk>/manage/', VendorContractManageView.as_view(), name='vendor_contract_manage'),
    path("contract/<int:pk>/delete/", VendorContractDeleteView.as_view(), name="vendor_contract_delete"),
    path("expiring/", ExpiringContractsListView.as_view(), name="contract_expire"),
    path('check-active-contract/', check_active_contract, name='check_active_contract'),



    # path('<int:pk>/', ContractDetailView.as_view(), name='contract_detail'),
    # path('<int:pk>/update/', ContractUpdateView.as_view(), name='contract_update'),
    # path('<int:pk>/delete/', ContractDeleteView.as_view(), name='contract_delete'),
]