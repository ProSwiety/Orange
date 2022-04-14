from django.urls import path
from . import views

urlpatterns = [
    path('inw/',views.inw_view, name='inw')
]