from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, TemplateView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from apps.user.models import Vendor
from .models import Document
from .forms import DocumentForm

class DocumentListView(ListView):
    model = Vendor
    template_name = 'documents/document_list.html'
    context_object_name = 'vendors'

    def get_queryset(self):
        return Vendor.objects.filter(documents__isnull=False).distinct()
        
class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('documents:document_list')

    def post(self, request, *args, **kwargs):
        # Get vendor from the main form
        vendor = request.POST.get('vendor')
        if not vendor:
            messages.error(request, "Vendor is required.")
            return self.form_invalid(self.get_form())

        # Create a list to hold created documents
        created_documents = []

        # Loop through POST data to find all dynamic fields
        counter = 1
        while True:
            doc_type_key = f'document_type_{counter}' if counter > 1 else 'document_type'
            file_key = f'file_{counter}' if counter > 1 else 'file'

            document_type = request.POST.get(doc_type_key)
            file = request.FILES.get(file_key)

            if not document_type and not file:
                # No more fields to process
                break

            if document_type and file:
                Document.objects.create(
                    vendor_id=vendor,
                    document_type=document_type,
                    file=file
                )
                created_documents.append(file)

            counter += 1

        if created_documents:
            messages.success(request, "Documents have been successfully uploaded!")
            return redirect(self.success_url)
        else:
            messages.error(request, "Please provide at least one document with a file.")
            return self.form_invalid(self.get_form())
        

class DocumentDeleteView(DeleteView):
    model = Document
    
    def get_success_url(self):
        # Redirect to the document detail page of the vendor
        document = self.get_object()
        vendor = document.vendor
        return reverse('documents:document_detail', kwargs={'pk': vendor.pk})
    
    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        document.delete()
        messages.success(request, "Document has been successfully deleted!")
        return JsonResponse({'success': True})


class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/edit_document.html' 
    
    def get_success_url(self):
        # Redirect to the document detail page of the vendor
        document = self.get_object()
        vendor = document.vendor
        return reverse('documents:document_detail', kwargs={'pk': vendor.pk})  # Placeholder, will be set in form_valid

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Document has been successfully updated!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the document.")
        return super().form_invalid(form)


class DocumentDetailView(DetailView):
    model = Vendor
    template_name = 'documents/document_detail.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.filter(vendor=self.object)
        return context

class VendorDocumentManageView(TemplateView):
    template_name = 'documents/vendor_document_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the vendor using the pk from the URL
        vendor_pk = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_pk)
        # Get all documents of the vendor
        context['vendor'] = vendor
        context['vendor_documents'] = Document.objects.filter(vendor=vendor)
        context['form'] = DocumentForm()  # Form for adding/updating documents
        context['document_type_choices'] = Document.DOCUMENT_TYPES  # Add this line
        return context

    def post(self, request, *args, **kwargs):
        vendor_pk = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_pk)

        # Handle adding or updating documents
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_id = request.POST.get('document_id')  # Check if updating an existing document
            if document_id:
                # Update existing document
                document = get_object_or_404(Document, id=document_id, vendor=vendor)
                document.file = form.cleaned_data['file']
                document.document_type = form.cleaned_data['document_type']
                document.save()
                messages.success(request, "Document updated successfully!")
            else:
                # Add new document
                Document.objects.create(
                    vendor=vendor,
                    file=form.cleaned_data['file'],
                    document_type=form.cleaned_data['document_type']
                )
                messages.success(request, "Document added successfully!")
        else:
            messages.error(request, "There was an error with the form. Please try again.")

        return redirect(reverse('documents:vendor_document_manage', kwargs={'pk': vendor.pk}))