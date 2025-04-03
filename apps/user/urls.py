from django.urls import path
from .views import user_vendor_list


urlpatterns = [
    path('vendor/', user_vendor_list, name='user_vendor_list'),
]
