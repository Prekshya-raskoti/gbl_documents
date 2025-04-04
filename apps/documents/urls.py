from django.urls import path
from .views import DocumentListView, DocumentCreateView, DocumentDeleteView

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentCreateView.as_view(), name='document_create'),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document_delete'),
]
