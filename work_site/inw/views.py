from django.shortcuts import render,redirect
from django.urls import reverse_lazy
import pandas as pd
from .models import InwModel
from .forms import upload_form,EditForm,CreateForm
from django.views.generic import DeleteView,UpdateView,CreateView
from django.contrib import messages


# Create your views here.

def create_value(request):
    if request.method == "POST":
        ean_form = CreateForm(request.POST)
        if ean_form.is_valid():
            ean_form.save()
        return redirect("myapp:table")
    ean_form = CreateForm()
    eans = InwModel.objects.all()
    return render(request=request, template_name="inw/inwmodel_create.html", context={'ean_form': ean_form, 'eans': eans})

class edit_value(UpdateView):
    UpdateView.model = InwModel
    UpdateView.fields = ['Ilosc']
    UpdateView.template_name_suffix = 'table.html'
    success_url = reverse_lazy('myapp:table')

class delete_ean(DeleteView):
    DeleteView.model = InwModel
    DeleteView.success_url = reverse_lazy('myapp:table')

def inw_view(request):
    if request.method == 'POST':
        sap_file = request.FILES['myfile']
        inw_file = request.FILES['inwfile']
        df = pd.read_excel(sap_file)
        dfi = pd.read_excel(inw_file)
        inw = dfi.iloc[:, 0].tolist()
        data_dict = dict()
        for col in df.columns:
            data_dict[col] = df[col].values.tolist()
        new_base = {
            'Nazwa': '',
            'EAN': '',
            'Ilosc': ''
        }
        for y in inw:
            if y in data_dict['EAN']:
                data_dict['Zapas ogółem'][data_dict['EAN'].index(y)] -= 1
        k = -1
        for y in data_dict['Zapas ogółem']:
            k += 1
            if y != 0:
                new_base['Ilosc'] = data_dict['Zapas ogółem'][k]
                new_base['EAN'] = data_dict['EAN'][k]
                new_base['Nazwa'] = data_dict['Krótki tekst materiału'][k]
                M = InwModel(**new_base)
                M.save()
        return redirect('/inw/table')
    else:
        return render(request,'inw/inw.html', {})

def table_view(request):
    values = InwModel.objects.all()
    context = {'values':values}
    return render(request,'inw/table.html', context)


def test_view(request):
    context = {}
    if request.method == 'POST':
        form = upload_form(request.POST, request.FILES)
        if form.is_valid():
            #func(request.FILES["upload_field"])
            pass
    else:
        form = upload_form()
    context['form'] = form
    return render(request, 'inw/test.html', context)


