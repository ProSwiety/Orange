from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('table/',views.TableData.as_view(), name='table'),
    path('upload/',views.UploadData.as_view(), name='upload'),
    path('create/',views.CreateData.as_view(), name='create'),
    path('delete/<int:pk>',views.DeleteData.as_view(), name='delete'),
    path('update/<int:pk>',views.UpdateView.as_view(), name='update'),
    path('test/',views.TestList.as_view())
]