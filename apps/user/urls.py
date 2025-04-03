from django.urls import path
from .views import VendorListView, VendorCreateView , VendorDeleteView

app_name = "user"

urlpatterns = [
    path('vendor/', VendorListView.as_view(), name='user_vendor_list'),  
    path('vendor/add/', VendorCreateView.as_view(), name='add_vendor'), 
    path('vendor/delete/<int:pk>/', VendorDeleteView.as_view(), name='delete_vendor'),
 

]
