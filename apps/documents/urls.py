from django.urls import path
from .views import DocumentListView, DocumentCreateView, DocumentDeleteView, VendorDocumentManageView, VendorDocumentDeleteView

app_name = 'documents'

urlpatterns = [
    path('list/', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentCreateView.as_view(), name='document_create'),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document_delete'),
    path('vendor/<int:pk>/manage/', VendorDocumentManageView.as_view(), name='vendor_document_manage'),
    path('vendor/<int:pk>/delete-documents/', VendorDocumentDeleteView.as_view(), name='vendor_document_delete'),




]
