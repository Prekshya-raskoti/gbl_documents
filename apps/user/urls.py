from django.urls import path
from .views import VendorListView, VendorCreateView

app_name = "user"

urlpatterns = [
    path('vendor/', VendorListView.as_view(), name='user_vendor_list'),  
    path('vendor/add/', VendorCreateView.as_view(), name='add_vendor'),  

]
