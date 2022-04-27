from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
import pandas as pd
from .models import InwModel
from .forms import UploadFileForm,EditForm,CreateDataForm
from django.views.generic import View,UpdateView,CreateView,DeleteView,ListView
from django.contrib import messages



# Create your views here.

class TestList(ListView):
    model = InwModel
    queryset = InwModel.objects.filter(Ilosc__lt=0)
    template_name = 'inw/test.html'

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
            index = -1
            for value in new_data['Zapas ogółem']:
                index += 1
                if value != 0:
                    sql_data['Ilosc'] = new_data['Zapas ogółem'][index]
                    sql_data['EAN'] = new_data['EAN'][index]
                    sql_data['Nazwa'] = new_data['Krótki tekst materiału'][index]
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
    def post(self,request):
        if 'check1' in request.POST and 'check2' in request.POST:
            values = InwModel.objects.all()
            context = {'values': values}
            return render(request, 'inw/table_form.html', context)
        elif 'check1' in request.POST:
            values = InwModel.objects.filter(Ilosc__lt=0)
            context = {'values': values}
            return render(request, 'inw/table_form.html', context)
        elif 'check2' in request.POST:
            values = InwModel.objects.filter(Ilosc__gt=0)
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









