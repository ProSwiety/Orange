from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserEmailForm, CustomPasswordChangeForm, CustomCreateUser, CustomResetPassword
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView
from django.views.generic import View, DeleteView, UpdateView, ListView
from django.contrib.auth.forms import PasswordResetForm
from inw.models import UploadModel, InwModel
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


# Create your views here.

class CreateUser(SuccessMessageMixin, View):

    def get(self, request):
        form = CustomCreateUser
        return render(request, 'accounts/create_user.html', context={'form': form})

    def post(self, request):
        form = CustomCreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Zarejestrowano Pomyślnie!")
            return redirect('home')
        else:
            form = CustomCreateUser
            messages.error(request, "Nie Zarejestrowano")
            return render(request, 'accounts/create_user.html', context={'form': form})


class CustomLoginView(LoginView):
    authentication_form = UserLoginForm


class ProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        model = UploadModel.objects.filter(user=request.user)
        context = {
            'model': model
        }
        return render(request, 'accounts/profile.html', context)


class DeleteModel(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'accounts/delete_model.html'
    model = UploadModel
    success_url = '/accounts/profile'
    success_message = f"Obiekt %(name)s %(date)s został usunięty!"
    login_url = '/login/'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
            date=self.object.date,
        )


class UpdateEmail(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/update_email.html'
    form_class = UserEmailForm
    success_url = '/accounts/profile'
    success_message = f"Email %(email)s został zaktualizowany!"
    login_url = '/login/'


class UploadModelList(LoginRequiredMixin, ListView):
    model = InwModel
    template_name = 'accounts/uploadmodel_list.html'

    def get_queryset(self):
        return InwModel.objects.filter(upload=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['model'] = UploadModel.objects.get(id=self.kwargs['pk'])
        return data


class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = '/accounts/profile'
    template_name = 'accounts/registration/password_change.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    model = User
    form_class = CustomResetPassword
    template_name = 'accounts/registration/password_reset_confirm.html'
    success_url = reverse_lazy('myauth:password_reset_complete')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Restart Hasła Web Inw"
                    email_template_name = "accounts/registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'proswiety.pythonanywhere.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    email_from = settings.EMAIL_HOST_USER
                    try:
                        send_mail(subject, email, email_from, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("done/")
    form = PasswordResetForm()
    return render(request=request, template_name="accounts/registration/password_reset.html",
                  context={"form": form})
