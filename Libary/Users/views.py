from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

# Create your views here.
def register(request):
    if request.method=="POST":
        username=request.POST["username"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        email=request.POST["email"]
        password=request.POST["pass1"]
        cpassword=request.POST["pass2"]
        if password==cpassword:
            u=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
            u.save()
        else:
            return HttpResponse("Password are not Matching try again")
        return redirect("Books:home")

    return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pass1']

        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('Books:home')
        else:
            return HttpResponse('<h1>invalid credentials</h1>')

    return  render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('Users:login')
