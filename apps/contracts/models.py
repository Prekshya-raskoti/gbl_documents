from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from apps.user.models import Vendor
class Contract(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contracts')
    join_date = models.DateField()
    expiry_date = models.DateField()
    terms_conditions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="contracts_created")

    def __str__(self):
        return f"Contract for {self.vendor.name} (Expires on {self.expiry_date})"
