from django.contrib import messages
from django.shortcuts import redirect ,render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,  DetailView
from .models import Vendor
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import VendorForm
from django.views import View
from django.db.models import Q
from django.utils.dateparse import parse_date

from django.views.generic import TemplateView
from django.utils import timezone
from .models import Vendor

from django.utils import timezone
from django.views.generic import TemplateView
from .models import Vendor 
from apps.contracts.models import Contract
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta
from django.views.generic import TemplateView
    
from django.http import JsonResponse
from django.template.loader import render_to_string
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        today = now.date()

        filter_param = self.request.GET.get('filter', 'all')
        search_query = self.request.GET.get('q', '')
        status_filter = self.request.GET.get('status', '')

        vendors = Vendor.objects.all()

        if search_query:
            vendors = vendors.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(address__icontains=search_query) 
            )

        if status_filter == 'expiring':
            vendors = vendors.filter(
                contracts__expiry_date__range=(today, today + timedelta(days=30))
            )

        if filter_param == 'today':
            vendors = vendors.filter(created_at__date=today)
        elif filter_param == 'expiring':
            expiring_vendor_ids = Contract.objects.filter(
                expiry_date__range=(today, today + timedelta(days=30))
            ).values_list('vendor_id', flat=True)
            vendors = vendors.filter(id__in=expiring_vendor_ids)

        vendors_with_status = []
        for vendor in vendors:
            contracts = vendor.contracts.all()  
            expiring_soon = contracts.filter(
                expiry_date__gte=today,
                expiry_date__lte=today + timedelta(days=30)
            ).exists()

            vendors_with_status.append({
                'vendor': vendor,
                'expiring_soon': expiring_soon
            })

        context.update({
            'total_vendors': vendors.count(),
            'total_vendors_today': vendors.filter(created_at__date=today).count(),
            'total_vendors_expiring': vendors.filter(contracts__expiry_date__range=(today, today + timedelta(days=30))).count(),
            'recent_vendors': vendors_with_status,
            'search_query': search_query,
            'filter_status': status_filter
        })

        return context
    
def filter_vendors_ajax(request):
    now = timezone.now()
    today = now.date()
    filter_param = request.GET.get('filter', 'all')
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    vendors = Vendor.objects.all()

    if search_query:
        vendors = vendors.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    if status_filter == 'expiring':
        vendors = vendors.filter(
            contracts__expiry_date__range=(today, today + timedelta(days=30))
        )

    if filter_param == 'today':
        vendors = vendors.filter(created_at__date=today)
    elif filter_param == 'expiring':
        expiring_vendor_ids = Contract.objects.filter(
            expiry_date__range=(today, today + timedelta(days=30))
        ).values_list('vendor_id', flat=True)
        vendors = vendors.filter(id__in=expiring_vendor_ids)

    vendors_with_status = []
    for vendor in vendors:
        contracts = vendor.contracts.all()  
        expiring_soon = contracts.filter(
            expiry_date__gte=today,
            expiry_date__lte=today + timedelta(days=30)
        ).exists()

        vendors_with_status.append({
            'vendor': vendor,
            'expiring_soon': expiring_soon
        })

    html = render_to_string('partials/vendor_table_rows.html', {'recent_vendors': vendors_with_status})
    return JsonResponse({'html': html})
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
            return redirect(reverse('dashboard'))
        elif hasattr(user, 'vendor_profile'):
            return redirect(reverse('user:user_vendor_list'))
        else:
            return redirect(reverse('user:user_vendor_list'))
        

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', reverse('dashboard'))
        return render(request, 'auth/logout_confirm.html', {'next': next_url})

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))

class VendorListView(ListView):
    model = Vendor
    template_name = 'user/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 5
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        queryset = Vendor.objects.all().order_by('-created_at')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
            )
        
        if from_date:
            queryset = queryset.filter(created_at__date__gte=parse_date(from_date))
        if to_date:
            queryset = queryset.filter(created_at__date__lte=parse_date(to_date))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_vendors'] = Vendor.objects.all().order_by('name')
        return context
    
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
    
class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'user/vendor_detail.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.object
        context['documents'] = vendor.documents.all()
        context['contracts'] = vendor.contracts.filter(is_active=True).prefetch_related('files')
        return context
    
    