from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
import pandas as pd
from .models import InwModel
from .forms import UploadFileForm,EditForm,CreateDataForm
from django.views.generic import View,UpdateView,CreateView,DeleteView
from django.contrib import messages


# Create your views here.

class UploadData(View):
    def get(self,request):
        form = UploadFileForm
        return render(request, 'inw/upload_form_page.html', {'form':form})

class TableData(View):
    def get(self,request):
        values = InwModel.objects.all()
        context = {'values': values}
        return render(request, 'inw/table.html', context)

class DeleteData(DeleteView):
    model = InwModel
    success_url = reverse_lazy('myapp:table')

#form dont load well change crispy to model form
class CreateData(CreateView):
    form = CreateDataForm
    model = InwModel
    fields =["Nazwa", "EAN", "Ilosc"]
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('myapp:table')









