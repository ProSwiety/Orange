from django.urls import path,include,reverse_lazy
from .views import CustomLoginView,ProfileView,DeleteModel,UpdateEmail
from django.contrib.auth import views as auth_views

app_name = 'myauth'

urlpatterns = [

path('profile/',ProfileView.as_view(), name='profile'),
path('delete_inw/<int:pk>',DeleteModel.as_view(), name='delete_inw'),
path('update_email/<int:pk>',UpdateEmail.as_view(), name='update_email'),
path('login/', CustomLoginView.as_view(template_name= 'accounts/registration/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('myauth:login')), name='logout'),
path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/registration/password_reset_form.html'), name='password_reset'),
path('confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
path('done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
path('complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),
#path("password_reset", views.password_reset_request, name="password_reset")

    ]