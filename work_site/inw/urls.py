from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('upload/',views.inw_view, name='inw'),
    path('table/',views.table_view, name='table'),
    path('test/',views.test_view, name='test'),
    path('delete_ean/<int:pk>',views.DeleteView.as_view(),name='delete_ean'),
    path('list_ean/',views.ListEan.as_view(),name='list')
]