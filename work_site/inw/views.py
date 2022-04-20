from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
import pandas as pd
from .models import InwModel
from .forms import UploadForm,EditForm,CreateForm
from django.views.generic import DeleteView,UpdateView,CreateView
from django.contrib import messages


# Create your views here.

def update_view(request,pk):
    context = {}
    obj = get_object_or_404(InwModel,id=pk)
    form = EditForm(request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect("myapp:table")
    context["form"] = form
    return render(request,"inw/update_view.html",context)

def create_value(request):
    if request.method == "POST":
        ean_form = CreateForm(request.POST)
        if ean_form.is_valid():
            ean_form.save()
            return redirect("myapp:table")
    ean_form = CreateForm()
    return render(request=request, template_name="inw/inwmodel_create.html", context={'ean_form': ean_form})

class delete_ean(DeleteView):
    DeleteView.model = InwModel
    DeleteView.success_url = reverse_lazy('myapp:table')

def inw_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('/inw/table')
    else:
        form = UploadForm()
        return render(request, 'inw/inw.html', {'form': form})
def table_view(request):
    values = InwModel.objects.all()
    context = {'values':values}
    return render(request,'inw/table.html', context)




