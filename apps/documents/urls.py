from django.urls import path
from .views import DocumentListView, DocumentCreateView, DocumentDeleteView, DocumentUpdateView, DocumentDetailView

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentCreateView.as_view(), name='document_create'),
    path('edit/<int:pk>/', DocumentUpdateView.as_view(), name='document_edit'),
    path('view/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document_delete'),


]
