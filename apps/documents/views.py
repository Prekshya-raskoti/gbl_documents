from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Document
from .forms import DocumentForm
from django.db.models import Q


class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10 

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        doc_type = self.request.GET.get('type', '')

        qs = Document.objects.all()

        if query:
            qs = qs.filter(
                Q(vendor__name__icontains=query)
            )

        if doc_type:
            qs = qs.filter(document_type=doc_type)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_types'] = Document.DOCUMENT_TYPES
        return context

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

class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'  # same form template as create
    success_url = reverse_lazy('documents:document_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Document has been successfully updated!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the document.")
        return super().form_invalid(form)

class DocumentDetailView(DetailView):
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'

