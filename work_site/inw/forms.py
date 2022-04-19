from django import forms

class upload_form(forms.Form):
    upload_field_sap = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }), label='Plik SAP')
    upload_field_inw = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }), label='Plik INW')
