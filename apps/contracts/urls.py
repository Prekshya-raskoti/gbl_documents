from django.urls import path
from .views import (
    ContractCreateView,
    ContractListView,
    VendorContractManageView,
    VendorContractDeleteView,
    ExpiringContractsListView,
    InactiveContractsListView,
    check_active_contract,
)

app_name = 'contracts'  
urlpatterns = [
    path('create/', ContractCreateView.as_view(), name='contract_create'),
    path('list/', ContractListView.as_view(), name='contract_list'),
    path('<int:pk>/manage/', VendorContractManageView.as_view(), name='vendor_contract_manage'),
    path("contract/<int:pk>/delete/", VendorContractDeleteView.as_view(), name="vendor_contract_delete"),
    path("expiring/", ExpiringContractsListView.as_view(), name="contract_expire"),
    path("inactive/", InactiveContractsListView.as_view(), name="contract_inactive"),
    path('check-active-contract/', check_active_contract, name='check_active_contract'),

]