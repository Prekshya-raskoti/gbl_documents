from django.shortcuts import render
from .models import User, Vendor

def user_vendor_list(request):
    return render(request, 'user/user_vendor_list.html')
