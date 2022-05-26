from django.shortcuts import render
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    authentication_form = UserLoginForm
