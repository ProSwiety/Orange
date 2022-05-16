from django import forms
from .models import InwModel,UploadModel



class UploadFileForm(forms.Form):
    upload_field_sap = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }),
        label='Plik SAP',
        label_suffix = '',
    )
    upload_field_inw = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class':"form-control mb-2 mr-sm-2",
        }),
        label='Plik INW',
        label_suffix='',
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
        fields = ["quantity"]
        widgets = {
            'quantity':forms.NumberInput()
        }

class CreateDataForm(forms.ModelForm):
    class Meta:
        model = InwModel
        fields = ["name", "EAN", "quantity", "upload"]
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Etui"}),
            'EAN': forms.NumberInput(attrs={'class':"form-control"}),
            'quantity': forms.NumberInput(attrs={'class':"form-control"}),
            'upload': forms.SelectMultiple(attrs={"class":"form-control"})
        }
        labels = {
            'quantity': ("Ilość")
        }


class UploadModelFormSelect(forms.ModelForm):
    class Meta:
        model = InwModel
        fields = ['upload']
        widgets = {
        'upload': forms.Select(attrs={
            "class": "form-select",
            'aria-label': "Default select example"})
        }
        labels = {
            'upload': ''
        }

    def __init__(self, user=None, **kwargs):
        super(UploadModelFormSelect, self).__init__(**kwargs)
        if user:
            self.fields['upload'].queryset = UploadModel.objects.filter(user=user)








