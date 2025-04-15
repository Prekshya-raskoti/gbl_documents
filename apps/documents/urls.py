from django.urls import path
from .views import DocumentListView, DocumentCreateView, DocumentDeleteView, DocumentUpdateView, DocumentDetailView, VendorDocumentManageView, VendorDocumentDeleteView

app_name = 'documents'

urlpatterns = [
    path('list/', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentCreateView.as_view(), name='document_create'),
    path('edit/<int:pk>/', DocumentUpdateView.as_view(), name='document_edit'),
    path('view/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document_delete'),
    path('vendor/<int:pk>/manage/', VendorDocumentManageView.as_view(), name='vendor_document_manage'),
    path('vendor/<int:pk>/delete-documents/', VendorDocumentDeleteView.as_view(), name='vendor_document_delete'),




]
