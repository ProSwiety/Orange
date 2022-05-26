from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


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
