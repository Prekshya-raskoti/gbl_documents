from django.urls import path
from .views import VendorListView, VendorCreateView ,VendorCreateFormView, VendorDeleteView , VendorUpdateView, VendorDetailView, filter_vendors_ajax

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "user"

urlpatterns = [
    path('vendor/', VendorListView.as_view(), name='user_vendor_list'),  
    path('api/vendor/add/', VendorCreateView.as_view(), name='api_add_vendor'), 
    path('vendor/add/', VendorCreateFormView.as_view(), name='add_vendor'),

    path('vendor/delete/<int:pk>/', VendorDeleteView.as_view(), name='delete_vendor'),
    path('vendor/<int:pk>/edit/', VendorUpdateView.as_view(), name='edit_vendor'),
    path('vendor/<int:pk>/detail/', VendorDetailView.as_view(), name='vendor_detail'),
    path('ajax/filter-vendors/', filter_vendors_ajax, name='filter_vendors_ajax'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

]
