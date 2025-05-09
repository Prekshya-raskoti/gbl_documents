from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy
from apps.user.models import Vendor
from .models import Document
from .forms import DocumentForm
from django.db.models import Q


class DocumentListView(ListView):
    model = Vendor
    template_name = 'documents/document_list.html'
    context_object_name = 'vendors'
    paginate_by = 10 

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        qs = Vendor.objects.filter(documents__isnull=False).distinct().order_by('-created_at')   

        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )

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

    def post(self, request, *args, **kwargs):
        vendor = request.POST.get('vendor')
        if not vendor:
            messages.error(request, "Vendor is required.")
            return self.form_invalid(self.get_form())

        created_documents = []

        # Loop through POST data to find all dynamic fields
        counter = 1
        while True:
            doc_type_key = f'document_type_{counter}' if counter > 1 else 'document_type'
            file_key = f'file_{counter}' if counter > 1 else 'file'

            document_type = request.POST.get(doc_type_key)
            file = request.FILES.get(file_key)

            if not document_type and not file:
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
        document = self.get_object()
        vendor = document.vendor
        return reverse('documents:vendor_document_manage', kwargs={'pk': vendor.pk})
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Vendor has been successfully deleted!")
        return super().post(request, *args, **kwargs)

class VendorDocumentManageView(TemplateView):
    template_name = 'documents/vendor_document_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor_pk = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_pk)
        context['vendor'] = vendor
        context['vendor_documents'] = Document.objects.filter(vendor=vendor).order_by('uploaded_at')
        context['form'] = DocumentForm() 
        context['document_type_choices'] = Document.DOCUMENT_TYPES  
        return context

    def post(self, request, *args, **kwargs):
        vendor_pk = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_pk)

        document_id = request.POST.get('document_id')
        print(f"Document ID: {document_id}")

        if document_id:
            # Update existing document
            document = get_object_or_404(Document, pk=document_id, vendor=vendor)
            form = DocumentForm(request.POST, request.FILES, instance=document)

            if form.is_valid():
                form.save()
                messages.success(request, "Document updated successfully!")
            else:
                print(form.errors)
                messages.error(request, "Error updating the document.")
        else:

        # Handle adding or updating documents
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                    Document.objects.create(
                        vendor=vendor,
                        file=form.cleaned_data['file'],
                        document_type=form.cleaned_data['document_type']
                    )
                    messages.success(request, "Document added successfully!")
            else:
                messages.error(request, "There was an error with the form. Please try again.")

        return redirect(reverse('documents:vendor_document_manage', kwargs={'pk': vendor.pk}))

class VendorDocumentDeleteView(View):
    def post(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        documents = Document.objects.filter(vendor=vendor)

        if documents.exists():
            count = documents.count()
            documents.delete()
            messages.success(request, f"Documents have been successfully deleted for vendor: {vendor.name}.")
        else:
            messages.info(request, f"No documents found for vendor: {vendor.name}.")

        return redirect('documents:document_list') 