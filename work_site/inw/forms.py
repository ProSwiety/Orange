from django import forms
from .models import InwModel


class upload_form(forms.Form):
    upload_field_sap = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }), label='Plik SAP')
    upload_field_inw = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }), label='Plik INW')

class EditForm(forms.Form):
    pass

class CreateForm(forms.ModelForm):
    class Meta:
        model = InwModel
        fields = ["Nazwa", "EAN", "Ilosc"]
        widgets = {
            'Nazwa': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Etui"}),
            'EAN': forms.NumberInput(attrs={'class':"form-control"}),
            'Ilosc': forms.NumberInput(attrs={'class':"form-control"})
        }
        labels = {
            'Ilosc': ("Ilość")
        }



