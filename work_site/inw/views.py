from django.shortcuts import render,redirect
from django.urls import reverse_lazy
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font,Alignment
from datetime import datetime
from .models import InwModel
from .forms import UploadFileForm,CreateDataForm
from django.views.generic import View,UpdateView,CreateView
from django.http import HttpResponse
from django.contrib import messages



# Create your views here.

def download_data_as_excel(request):
    model_queryset = InwModel.objects.all()
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%Y-%m-%d')}-akcesoria.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Akcesoria'
    columns = [
        'ID',
        'Nazwa',
        'EAN',
        'Ilość',
    ]
    row_num = 1
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        wsc = worksheet[cell.coordinate]
        cell.value = column_title
        column_letter = get_column_letter(col_num)
        column_dimensions = worksheet.column_dimensions[column_letter]
        wsc.font = Font(bold=True, size="13")
        wsc.alignment = Alignment(horizontal='center', vertical='center')
        worksheet.row_dimensions[1].height = 35
        if column_title == 'ID' or column_title == 'Ilość':
            column_dimensions.width = 8
        elif column_title == 'EAN':
            column_dimensions.width = 20
        else:
            column_dimensions.width = 40
    for model in model_queryset:
        row_num += 1
        row = [
            row_num - 1,
            model.Nazwa,
            model.EAN,
            model.Ilosc,
        ]
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            wsc = worksheet[cell.coordinate]
            if cell.column_letter == 'A':
                wsc.alignment = Alignment(horizontal='left')
            elif cell.column_letter == 'C':
                wsc.alignment = Alignment(horizontal='center')
            elif cell.column_letter == 'D':
                if cell_value > 0:
                    wsc.font = Font(color="0000FF00")
                elif cell_value < 0:
                    wsc.font = Font(color="00FF0000")
            cell.value = cell_value
    worksheet.auto_filter.ref = worksheet.dimensions
    workbook.save(response)
    return response

def confirm_delete_list(request):
    if request.method == 'GET':
        id_list = request.GET.getlist('delete')
        objects = InwModel.objects.filter(id__in=id_list)
        return render(request, 'inw/inwmodel_delete_list.html', {'objects':objects})
    if request.method == 'POST':
        id_list = request.GET.getlist('delete')
        objects = InwModel.objects.filter(id__in=id_list).delete()
        return redirect('/inw/table')

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
        if 'check1' in request.GET or 'check2' in request.GET:
            if 'check1' in request.GET:
                values = InwModel.objects.filter(Ilosc__lt=0)
                context = {'values': values}
                return render(request, 'inw/table_form.html', context)
            elif 'check2' in request.GET:
                values = InwModel.objects.filter(Ilosc__gt=0)
                context = {'values': values}
                return render(request, 'inw/table_form.html', context)
            else:
                values = InwModel.objects.all()
                context = {'values': values}
                return render(request, 'inw/table_form.html', context)
        else:
            values = InwModel.objects.all()
            context = {'values': values}
            return render(request, 'inw/table_form.html', context)

def table_sort_up(request):
    values = InwModel.objects.order_by('-Ilosc')
    context = {'values': values}
    return render(request, 'inw/table_form.html', context)

def table_sort_down(request):
    values = InwModel.objects.order_by('Ilosc')
    context = {'values': values}
    return render(request, 'inw/table_form.html', context)



#form dont load well change crispy to model form
class CreateData(CreateView):
    form = CreateDataForm
    model = InwModel
    fields =["Nazwa", "EAN", "Ilosc"]
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('myapp:table')









