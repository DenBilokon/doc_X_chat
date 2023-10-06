from django import forms
from .models import PDFDocument


class PDFDocumentForm(forms.ModelForm):

    class Meta:
        model = PDFDocument
        fields = ['title', 'embedding']


class PDFDocumentForm2(forms.ModelForm):

    class Meta:
        model = PDFDocument
        fields = ['title', 'documentContent', 'embedding']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'documentContent': forms.Textarea(attrs={'class': 'form-control'}),
            'embedding': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'documentContent': 'Document Content',
            'embedding': 'Embedding',
        }


class PDFUpdateForm(forms.ModelForm):

    class Meta:
        model = PDFDocument
        fields = ['title', 'documentContent', 'embedding']


class PDFUploadForm(forms.Form):

    pdf_document = forms.FileField(label='Upload a PDF', required=True)