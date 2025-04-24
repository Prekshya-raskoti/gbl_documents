from django.contrib import messages
from django.shortcuts import redirect ,render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Vendor
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import VendorForm
from django.views import View
from django.db.models import Q
from django.utils.dateparse import parse_date

class LoginView(View):
    template_name = 'auth/login.html' 
    
    def get(self, request):
        if request.user.is_authenticated:
            return self.redirect_authenticated_user(request.user)  
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            return self.redirect_authenticated_user(user)
        else:
            return render(request, self.template_name, {'form': form})
    
    def redirect_authenticated_user(self, user):
        if user.is_superuser:
            return redirect(reverse('user:user_vendor_list'))
        elif hasattr(user, 'vendor_profile'):
            return redirect(reverse('user:user_vendor_list'))
        else:
            return redirect(reverse('user:user_vendor_list'))
        
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('login'))
    else:
        return render(request, 'auth/logout_confirm.html')

class VendorListView(ListView):
    model = Vendor
    template_name = 'user/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        queryset = Vendor.objects.all().order_by('id')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
            )

        if from_date:
            queryset = queryset.filter(created_at__date__gte=parse_date(from_date))
        if to_date:
            queryset = queryset.filter(created_at__date__lte=parse_date(to_date))

        return queryset
    
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
    template_name = 'user/delete_vendor.html'
    success_url = reverse_lazy('user:user_vendor_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Vendor has been successfully deleted!")
        return super().post(request, *args, **kwargs)
    
    