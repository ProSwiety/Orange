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
    def post(self, request, *args, **kwargs):
        from .upload_scripts.upload_scripts import excel_inf_to_list, excel_sap_to_dict, process_excel_files
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            df_sap = pd.read_excel(request.FILES['upload_field_sap'])
            df_inw = pd.read_excel(request.FILES['upload_field_inw'])
            inw_list = excel_inf_to_list(df_inw)
            sap_dict = excel_sap_to_dict(df_sap)
            new_data = process_excel_files(inw_list,sap_dict)
            sql_data = {
                'Nazwa': '',
                'EAN': '',
                'Ilosc': ''
            }
            number = -1
            for keys in new_data['Ilosc']:
                number += 1
                sql_data['Ilosc'] = new_data['Ilosc'][number]
                sql_data['EAN'] = new_data['EAN'][number]
                sql_data['Nazwa'] = new_data['Nazwa'][number]
                model = InwModel(**sql_data)
                model.save()
        return redirect('/inw/table')

class EditData(UpdateView):
    UpdateView.model = InwModel
    UpdateView.fields = ['Ilosc']
    UpdateView.template_name_suffix = '_update_form'
    UpdateView.success_url = reverse_lazy('myapp:table')

class TableData(View):
    def get(self,request):
        values = InwModel.objects.all()
        context = {'values': values}
        return render(request, 'inw/table_form.html', context)

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









