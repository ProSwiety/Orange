from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('upload/',views.inw_view, name='inw'),
    path('table/',views.table_view, name='table'),
    path('delete_ean/<int:pk>',views.DeleteView.as_view(),name='delete_ean'),
    path('create_ean/',views.create_value,name='create_ean'),
    path('update/<int:pk>',views.update_view,name='update')
]