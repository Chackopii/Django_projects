from django.shortcuts import render,redirect,reverse
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.
def categories(request):

    category =Category.objects.all()

    context={
        'categories':category
    }
    return render(request,'category.html',context)

def add_category(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        des = request.POST['description']
        image = request.FILES.get('image')  # FILE for image and documents# FILE for image and documents
        form = Category.objects.create(name=name,des=des,img=image)  # an new record is added
        form.save()  # same as form.commit()
        return redirect('Shop:categories')

    return render(request,"add_category.html")


def product(request,pk):

    category=Category.objects.get(id=pk)

    product=Product.objects.filter(category=category)

    context={'category':category,'product':product}

    return render(request,'product.html',context)


def add_product(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        image = request.FILES.get('image')
        des = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        cat=request.POST['category']
        try:
            category = Category.objects.get(name=cat)
            form = Product.objects.create(name=name,img=image,des=des,price=price,stock=stock,category=category)  # an new record is added
            form.save()  # same as form.commit()
            return redirect('Shop:categories')
        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
    return render(request,"add_product.html")


def productdetail(request,pk):

    product=Product.objects.get(id=pk)

    context={'product':product}

    return render(request,'detail.html',context)

def add_stock(request,pk):
    product=Product.objects.get(id=pk)
    if request.method == "POST":
        product.stock=request.POST['stock']
        product.save()
        return redirect(reverse('Shop:detail',args=pk))

    context={
        "product":product
    }
    return render(request,'add_stock.html',context)

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
        return redirect("Shop:login")

    return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pass1']

        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('Shop:categories')
        else:
            return HttpResponse('invalid credentials')

    return  render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('Shop:login')


def searchitem(request):
    searchitem = None
    query = ''
    if request.method == 'POST':
        query = request.POST['search']
        if query:
            searchitem = Product.objects.filter(Q(name__icontains=query))  # Q is used to when logical operation are needed in django application only after Q |,and,or are used

    return render(request, 'search.html', {"search": searchitem, "query": query})
