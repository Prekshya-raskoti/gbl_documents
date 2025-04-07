from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView ,CreateView , DeleteView ,UpdateView
from .models import Vendor
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .forms import VendorForm
from django.contrib.auth import logout
from django.views import View
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
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
                
            return self.redirect_authenticated_user(user)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, self.template_name, {'form': form})
    
    def redirect_authenticated_user(self, user):
        if user.is_superuser:
            return redirect(reverse('user:user_vendor_list'))
        elif hasattr(user, 'vendor_profile'):
            return redirect(reverse('user:user_vendor_list'))
        else:
            return redirect(reverse('user:user_vendor_list'))  # Redirect to a different page for other users

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect(reverse('login'))

# def custom_login_view(request):
#     if request.user.is_authenticated:
#         return redirect(reverse('user:user_vendor_list'))

#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect(reverse('user:user_vendor_list'))
#         else:
#             form = AuthenticationForm()

#         return render(request, 'registration/login.html', {'form': form})
#     form = AuthenticationForm(request, data=request.POST)
#     return render(request, 'registration/login.html', {'form': form})
    
# def logout_view(request):
#     logout(request)  
#     return redirect(reverse('user:logged_out')) 

# def logged_out_view(request):
#     return render(request, 'registration/logged_out.html')  

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