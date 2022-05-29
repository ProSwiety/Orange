from django.urls import path, include, reverse_lazy
from .views import CustomLoginView, ProfileView, DeleteModel, UpdateEmail, PasswordChange, UploadModelList, CreateUser, \
    password_reset_request, PasswordResetConfirm
from django.contrib.auth import views as auth_views

app_name = 'myauth'

urlpatterns = [

    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_inw/<int:pk>', DeleteModel.as_view(), name='delete_inw'),
    path('update_email/<int:pk>', UpdateEmail.as_view(), name='update_email'),
    path('list/<int:pk>', UploadModelList.as_view(), name='list'),
    path('login/', CustomLoginView.as_view(template_name='accounts/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('myauth:login')), name='logout'),
    path('password_change/<int:pk>', PasswordChange.as_view(), name='password_change'),
    path('password_reset/', password_reset_request,
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),
    # path("password_reset", views.password_reset_request, name="password_reset")

]
