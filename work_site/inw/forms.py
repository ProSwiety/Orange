from django import forms
from .models import InwModel


class UploadFileForm(forms.Form):
    upload_field_sap = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }),
        label='Plik SAP',
        label_suffix = ''
    )
    upload_field_inw = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }),
        label='Plik INW',
        label_suffix=''
    )

class SurplusLackInputForm(forms.Form):
    lack_check = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class':"form-check-input",
        'id':"radio-lack",
        'role':"switch",
        'value':"lack"
    }),
        label="Braki",
        label_suffix=''
    )

    surplus_check = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class': "form-check-input",
        'id': "radio-lack",
        'role': "switch",
        'value': "surplus"
    }),
        label="Nadwyżki",
        label_suffix=''
    )

class EditForm(forms.ModelForm):
    class Meta:
        model = InwModel
        fields = ["Ilosc"]
        widgets = {
            'Ilosc':forms.NumberInput()
        }

class CreateDataForm(forms.ModelForm):
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



