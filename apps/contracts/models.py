from django.db import models
from django.conf import settings
from apps.user.models import Vendor

class Contract(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contracts')
    join_date = models.DateField()
    expiry_date = models.DateField()
    terms_conditions = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="contracts_created")
    

    def __str__(self):
        return f"Contract for {self.vendor.name} (Expires on {self.expiry_date})"

class ContractFile(models.Model):
    file = models.FileField(upload_to='vendor_contracts/')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="contract_files_uploaded")

    def __str__(self):
        return f"Contract document for {self.contract.vendor.name} (Expires on {self.uploaded_at})"