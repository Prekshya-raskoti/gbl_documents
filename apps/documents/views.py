from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Document
from .forms import DocumentForm

class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'

class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('documents:document_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Document has been successfully uploaded!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with the form submission.")
        return super().form_invalid(form)

class DocumentDeleteView(DeleteView):
    model = Document
    success_url = reverse_lazy('documents:document_list')

    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        document.delete()
        messages.success(request, "Document has been successfully deleted!")
        return JsonResponse({'success': True})
