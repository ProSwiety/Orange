from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('table/',views.TableData.as_view(), name='table'),
    path('upload/',views.UploadData.as_view(), name='upload'),
    path('create/',views.CreateData.as_view(), name='create'),
    path('update/<int:pk>',views.UpdateView.as_view(), name='update'),
    path('table/delete',views.confirm_delete_list, name='list'),
    path('download/',views.download_data_as_excel, name='download'),
]

handler404 = "work_site.views.page_not_found_view"

