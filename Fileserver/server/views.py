from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import MyFORM
from .models import DBase
from django.db.models import Q
import os
from Fileserver.settings import PROJECT_DIR
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

@login_required
def index(request):
    message ={'Message': False,'search':" ",'Searched':False,"user":request.user.username}
    if request.method=='POST':
        form = MyFORM(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            extension=os.path.splitext(str(request.FILES['File']))[1]
            DBase(Tag=data["Tag"],Author=request.user.username, File=data["File"],Ext=extension).save()
        else:
            message["Message"]=True
    data = DBase.objects.all()
    message["data"]=data
    return render(request,'index.html',message)

@login_required
def upload(request):
    message ={"user":request.user.username}
    return render(request,'upload.html',message)

@login_required
def delete(request):
    if request.method=='POST':
        x = request.POST.get('x','')
        logs = DBase.objects.get(pk=x)
        if(logs.Author == request.user.username or request.user.is_superuser):
            try:
                os.remove(PROJECT_DIR+logs.File.url)
            except OSError:
                pass
            logs.delete()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')

    else:
        return HttpResponse('failure')

@login_required
def search(request):
    message ={'Message': False,'search':" ",'Searched':False,"user":request.user.username}
    if request.method=='POST':
        x = request.POST.get('search','')
        s = DBase.objects.all().filter(Q(Tag=x) | Q(Author=x))
        message["data"]=s
        message["search"]="Your Search Result: "+str(len(s))+" results found."
        message['Searched']=True
        return render(request,'index.html',message)
    else:
        message["data"]= null
        return render(request,'index.html',message)


def register(request):
    if request.method=='POST':
        Username = request.POST.get("Username","")
        Password = request.POST.get("Password","")
        Firstname = request.POST.get("Firstname","")
        Lastname = request.POST.get("Lastname","")
        Email = request.POST.get("Email","")
        try:
            user = User.objects.create_user(username=Username,email=Email,password=Password,first_name=Firstname, last_name=Lastname)
            user.save()
            login(request,user)
            return HttpResponse("Success")
        except:
            return HttpResponse("Username already exist")
    else:
        return HttpResponse("Failed to register.")


def validate(request):
    if request.method=='POST':
        Username = request.POST.get("Username","")
        Password = request.POST.get("Password","")
        user = authenticate(username=Username,password=Password)

        if user==None:
            return HttpResponse("Failed to Log in")
        else:
            login(request,user)
            return HttpResponse("Success")

    else:
        return HttpResponse("Invalid Page!!!")

@login_required
def Log_out(request):
    logout(request)
    return render(request,"login.html")
