from django import forms
from .models import InwModel, UploadModel


class SurplusLackInputForm(forms.Form):
    lack_check = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class': "form-check-input",
        'id': "radio-lack",
        'role': "switch",
        'value': "lack"
    }),
        label= "Braki",
        label_suffix= ''
)

    surplus_check = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class': "form-check-input",
        'id': "radio-lack",
        'role': "switch",
        'value': "surplus"
    }),
        label= "Nadwyżki",
        label_suffix= ''
)


class EditForm(forms.ModelForm):
    class Meta:
        model = InwModel
        fields = ["quantity"]
        widgets = {
            'quantity': forms.NumberInput()
        }
        labels = {
            'quantity': 'Ilość',
        }


class CreateDataForm(forms.ModelForm):
    class Meta:
        model = InwModel
        fields = ["name", "EAN", "quantity", "upload"]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Etui"}),
            'EAN': forms.NumberInput(attrs={'class': "form-control", 'placeholder': "123456789"}),
            'quantity': forms.NumberInput(attrs={'class': "form-control"}),
            'upload': forms.Select(attrs={"class": "form-control", }),
        }
        labels = {
            'name': 'Nazwa',
            'quantity': 'Ilość',
            'upload': 'Zbiór',
        }
        help_texts = {
            'upload': 'Wymagane jest wybranie któregoś z zbiorów',
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
