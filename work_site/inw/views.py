from django.shortcuts import render

# Create your views here.

def inw_view(request):
    return render(request,'inw/inw.html')
