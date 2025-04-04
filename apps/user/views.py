from django.contrib import messages
from django.views.generic import ListView ,CreateView , DeleteView ,UpdateView
from .models import Vendor
from django.urls import reverse_lazy
from .forms import VendorForm

class VendorListView(ListView):
    model = Vendor
    template_name = 'user/user_vendor_list.html'
    context_object_name = 'vendors'
    
class VendorCreateView(CreateView):
    model = Vendor
    form_class = VendorForm  
    template_name = 'user/vendor_form.html'
    success_url = reverse_lazy('user:user_vendor_list')  

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Vendor has been successfully created!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with the form submission.")
        return super().form_invalid(form)   

class VendorUpdateView(UpdateView):
    model = Vendor
    fields = ['name', 'email', 'address', 'phone']
    template_name = 'user/edit_vendor.html'  
    success_url = reverse_lazy('user:user_vendor_list')       
   
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Vendor details updated successfully!")
        return response
class VendorDeleteView(DeleteView):
    model = Vendor
    success_url = reverse_lazy('user:user_vendor_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Vendor has been successfully deleted!")
        return super().post(request, *args, **kwargs)