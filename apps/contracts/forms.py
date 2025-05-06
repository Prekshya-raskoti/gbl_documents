from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from .models import Contract, ContractFile


class ContractForm(forms.ModelForm):
    files = forms.CharField(
        widget=forms.HiddenInput(),  # This will store file paths as a hidden input
        required=False,
    )
    

    class Meta:
        model = Contract
        fields = ['vendor', 'join_date', 'expiry_date']
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'join_date': 'Contract Expiry Date',
            'expiry_date': 'Contract Expiry Date',
        }
        

    def clean_files(self):
        """Manually process files and store file paths"""
        files = self.files.getlist("files")  # Get the list of files
        if not files:
            return None  # No files selected
        return files

    def save(self, commit=True):
        
        contract = super().save(commit=commit)
        # Manually save the files if any
        files = self.cleaned_data.get("files")
        if files:
            self.save_uploaded_files(contract, files)
        return contract

    def save_uploaded_files(self, contract, files):
        for f in files:
            ContractFile.objects.create(contract=contract, file=f,uploaded_by=contract.created_by)
