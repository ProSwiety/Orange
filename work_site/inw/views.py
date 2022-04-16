from django.shortcuts import render


# Create your views here.

def inw_view(request):
    import pandas as pd
    if request.method == 'POST':
        excel_file = request.FILES['myfile']
        df = pd.read_excel(excel_file)
        dict = df.to_dict('split')

        return render(request, 'inw/inw.html', {"dict": dict})
    else:
        return render(request,'inw/inw.html', {})
