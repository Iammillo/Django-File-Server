from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyFORM
from .models import DBase
from django.db.models import Q
import os


def index(request):
    message ={'Message': False,'search':" ",'Searched':False,}
    if request.method=='POST':
        form = MyFORM(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            extension=os.path.splitext(str(request.FILES['File']))[1]
            DBase(Tag=data["Tag"],Author=data["Author"], File=data["File"],Ext=extension).save()
        else:
            message["Message"]=True
    data = DBase.objects.all()
    message["data"]=data
    return render(request,'index.html',message)


def upload(request):
    return render(request,'upload.html')

def delete(request):
    if request.method=='POST':
        x = request.POST.get('x','')
        DBase.objects.all().filter(pk=x).delete()
        return HttpResponse('success')
    else:
        return HttpResponse('failure')


def search(request):
    message ={'Message': False,'search':" ",'Searched':False,}
    if request.method=='POST':
        x = request.POST.get('x','')
        s = DBase.objects.all().filter(Q(Tag=x) | Q(Author=x))
        message["data"]=s
        message["search"]="Your Search Result: "+str(len(s))+" results found."
        message['Searched']=True
        return render(request,'index.html',message)
    else:
        message["data"]= null
        return render(request,'index.html',message)
