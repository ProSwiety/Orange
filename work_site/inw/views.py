from django.shortcuts import render


# Create your views here.

def inw_view(request):
    import openpyxl
    if request.method == 'POST':
        excel_file = request.FILES['myfile']
        wb_obj = openpyxl.load_workbook(excel_file)
        sheet = wb_obj.get_sheet_by_name('Arkusz1')
        dict = {col[0]: col[1:] for col in zip(*sheet.values)}
        return render(request, 'inw/inw.html', {"dict": dict})
    else:
        return render(request,'inw/inw.html', {})
