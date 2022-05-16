from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font,Alignment
from datetime import datetime
from .models import InwModel,UploadModel
from .forms import UploadFileForm,CreateDataForm,SurplusLackInputForm,UploadModelFormSelect
from django.views.generic import View,UpdateView,CreateView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

@login_required(login_url="/login")
def download_data_as_excel(request):
    user_query = UploadModel.objects.filter(user=request.user)
    model_queryset = InwModel.objects.filter(upload=user_query)
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

@login_required(login_url="/login")
def confirm_delete_list(request):
    if request.method == 'GET':
        id_list = request.GET.getlist('delete')
        if len(id_list) == 0:
            messages.add_message(request, messages.ERROR, 'You must select the item to be deleted')
            return redirect('/inw/table')
        else:
            objects = InwModel.objects.filter(id__in=id_list)
            return render(request, 'inw/inwmodel_delete_list.html', {'objects':objects})
    if request.method == 'POST':
        id_list = request.GET.getlist('delete')
        InwModel.objects.filter(id__in=id_list).delete()
        messages.add_message(request, messages.SUCCESS, 'Delete')
        return redirect('/inw/table')


class UploadData(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        form = UploadFileForm
        return render(request, 'inw/upload_form_page.html', {'form':form})
    def post(self, request, *args, **kwargs):
        from .upload_scripts.upload_scripts import excel_inf_to_list, excel_sap_to_dict, process_excel_files
        from .upload_scripts.user_query_check_NaN import check_NaN
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                user = request.user
                df_sap = pd.read_excel(request.FILES['upload_field_sap'])
                df_inw = pd.read_excel(request.FILES['upload_field_inw'])
                inw_list = excel_inf_to_list(df_inw)
                sap_dict = excel_sap_to_dict(df_sap)
                new_data = process_excel_files(inw_list,sap_dict)
                user_query = UploadModel.objects.filter(user=user)
                name = check_NaN(user_query)
                upload_file = UploadModel(name=name, user=user)
                upload_file.save()
                sql_data = {
                    'name': '',
                    'EAN': '',
                    'quantity': '',
                    'upload': upload_file
                }
                index = -1
                for value in new_data['Zapas ogółem']:
                    index += 1
                    if value != 0:
                        sql_data['quantity'] = new_data['Zapas ogółem'][index]
                        sql_data['EAN'] = new_data['EAN'][index]
                        sql_data['name'] = new_data['Krótki tekst materiału'][index]
                        model = InwModel(**sql_data)
                        model.save()
                return redirect('/inw/table')
            except:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak')
                return render(request, 'inw/upload_form_page.html', {'form':form})




class TableData(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
            forms = SurplusLackInputForm()
            upload_form = UploadModelFormSelect()
            upload_form.instance.upload.user = request.user
            uploads = UploadModel.objects.filter(user=request.user)
            if upload_form.is_valid:
                if forms.is_valid:
                    try:
                        upload_model_id = UploadModel.objects.get(id=request.GET['upload'])
                        values = InwModel.objects.filter(upload=upload_model_id)
                        intaial_data = {
                            'upload': upload_model_id,
                        }
                        upload_form = UploadModelFormSelect(initial=intaial_data)
                        if 'lack_check' in request.GET and 'surplus_check' in request.GET:
                            context = {'values': values, 'forms': forms, 'uploads':uploads, 'upload_form':upload_form}
                            return render(request, 'inw/table_form.html', context)
                        elif 'lack_check' in request.GET:
                            forms.fields['surplus_check'].initial = False
                            values = values.filter(quantity__lt=0)
                            context = {'values': values, 'forms': forms, 'uploads':uploads, 'upload_form':upload_form}
                            return render(request, 'inw/table_form.html', context)
                        elif 'surplus_check' in request.GET:
                            forms.fields['lack_check'].initial = False
                            values = values.filter(quantity__gt=0)
                            context = {'values': values, 'forms': forms, 'uploads':uploads, 'upload_form':upload_form}
                            return render(request, 'inw/table_form.html', context)
                    except:
                        default_upload = uploads.latest('name')
                        values = InwModel.objects.filter(upload=default_upload)
                        intaial_data = {
                            'upload': default_upload,
                        }
                        upload_form = UploadModelFormSelect(initial=intaial_data)
                        context = {'values': values, 'forms': forms, 'uploads':uploads, 'upload_form':upload_form}
                        return render(request, 'inw/table_form.html', context)



class InwModelCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    form = CreateDataForm
    model = InwModel
    fields =["name", "EAN", "quantity", 'upload']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('myapp:table')
    success_message = "%(name)s was created succesfully"
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super(InwModelCreateView, self).get_form_kwargs()
        kwargs['upload'] = self.request.user
        return kwargs



class InwModelUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = InwModel
    fields = ['name', 'quantity']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('myapp:table')
    success_message = f"%(name)s was editing succesfully"
    login_url = '/login/'


    









