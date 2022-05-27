from django.shortcuts import render
from .forms import UserLoginForm,UserEmailForm
from django.contrib.auth.views import LoginView
from django.views.generic import View, DeleteView, UpdateView
from inw.models import UploadModel
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.

class CustomLoginView(LoginView):
    authentication_form = UserLoginForm

class ProfileView(View):

    def get(self,request):
        model = UploadModel.objects.filter(user=request.user)
        context = {
            'model': model
        }
        return render(request, 'accounts/profile.html', context)

class DeleteModel(DeleteView):
    template_name = 'accounts/delete_model.html'
    model = UploadModel
    success_url = '/accounts/profile'

class UpdateEmail(UpdateView):
    model = User
    template_name = 'accounts/update_email.html'
    form_class = UserEmailForm
    success_url = '/accounts/profile'

