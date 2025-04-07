from django.db import models
from  apps.user.models import Vendor

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('citizenship', 'Citizenship'),
        ('Citizenship Back', 'Citizenship Back'),
        ('bank_details', 'Bank Details'),
        ('pan_card', 'PAN Card'),
        ('other', 'Other'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='vendor_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.vendor.name} - {self.get_document_type_display()}"
