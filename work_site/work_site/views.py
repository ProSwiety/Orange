from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView

class HomeView(TemplateView):
    template_name = 'home.html'

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

class CustomLoginView(LoginView):
    authentication_form = UserLoginForm
