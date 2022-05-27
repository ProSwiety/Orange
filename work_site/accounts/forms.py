from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User



class UserEmailForm(ModelForm):

    email = forms.EmailField(required=True,widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('email',)

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control'
               }),
        label="Nazwa Użytkownika",
        label_suffix='',


    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'

        }),
        label="Hasło",
        label_suffix=''
    )
