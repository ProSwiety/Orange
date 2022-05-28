from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm, UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class CustomCreateUser(UserCreationForm):
    username = forms.CharField(required=True, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control'}),
                               label="Nazwa Salonu",
                               )

    email = forms.EmailField(required=True, widget=forms.TextInput,
                             label="Email Salonu",
                             )

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}),
        label="Hasło",
        label_suffix='',
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}),
        label="Powtórz Hasło",
        label_suffix='',
    )
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def save(self, commit=True):
        user = super(CustomCreateUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserEmailForm(ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('email',)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}),
        label="Stare Hasło",
        label_suffix='',
    )
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}),
        label="Nowe Hasło",
        label_suffix='',
        help_text=f'Wymagane jest wybranie któregoś z zbiorów'

    )
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}),
        label="Potwierdź Nowe Hasło",
        label_suffix='',

    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


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
