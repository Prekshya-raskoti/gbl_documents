from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['vendor', 'document_type', 'file']

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['vendor'].widget.attrs.update({'class': 'select2 form-control'})
