from django.urls import path
from .views import DocumentListView, DocumentCreateView, DocumentDeleteView, VendorDocumentManageView, VendorDocumentDeleteView, CheckDocumentExistsView, SecureDocumentView

app_name = 'documents'

urlpatterns = [
    path('list/', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentCreateView.as_view(), name='document_create'),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document_delete'),
    path('<int:pk>/manage/', VendorDocumentManageView.as_view(), name='vendor_document_manage'),
    path('vendor/<int:pk>/delete-documents/', VendorDocumentDeleteView.as_view(), name='vendor_document_delete'),
    path('check-document-exists/', CheckDocumentExistsView.as_view(), name='check_document_exists'),
    path('document/<int:document_id>/view/', SecureDocumentView.as_view(), name='secure_document_view'),
]
