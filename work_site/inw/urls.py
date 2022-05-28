from django.urls import path
from .views import TableData, UploadData, InwModelCreateView, InwModelUpdateView, ConfirmDeleteList, \
    download_data_as_excel

app_name = 'myapp'

urlpatterns = [
    path('table/', TableData.as_view(), name='table'),
    path('upload/', UploadData.as_view(), name='upload'),
    path('create/', InwModelCreateView.as_view(), name='create'),
    path('update/<int:pk>', InwModelUpdateView.as_view(), name='update'),
    path('delete/', ConfirmDeleteList.as_view(), name='list'),
    path('download/', download_data_as_excel, name='download'),
    path('download/<int:pk>', download_data_as_excel, name='download'),

]

handler404 = "work_site.views.page_not_found_view"
