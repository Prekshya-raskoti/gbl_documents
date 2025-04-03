from django.shortcuts import render
from django.views.generic import ListView ,CreateView
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
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)    
   