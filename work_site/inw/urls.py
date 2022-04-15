from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('inw/',views.inw_view, name='inw')
]