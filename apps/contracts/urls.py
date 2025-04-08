from django.urls import path
from .views import (
    ContractDetailView,
    ContractCreateView,
    ContractUpdateView,
    ContractDeleteView,
)
from . import views

app_name = 'contracts'

urlpatterns = [
    path('list/', views.contract_list, name='contract_list'),
    path('create/', ContractCreateView.as_view(), name='contract_create'),
    path('<int:pk>/', ContractDetailView.as_view(), name='contract_detail'),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name='contract_update'),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name='contract_delete'),
]
