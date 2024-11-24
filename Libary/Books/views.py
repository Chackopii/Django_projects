from django.shortcuts import render,redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request,'home.html')
@login_required
def add_book(request):
    if(request.method=='POST'):
        title=request.POST['title']
        author=request.POST['author']
        language=request.POST['language']
        price=request.POST['price']
        pages=request.POST['pages']
        cover=request.FILES.get('cover') #FILE for image and documents
        pdf=request.FILES.get('pdf') #FILE for image and documents
        form=Book.objects.create(title=title,author=author,Language=language,price=price,pages=pages,cover=cover,pdf=pdf) #an new record is added
        form.save() #same as form.commit()
        return redirect('Books:view_book')

    return render(request,'add_book.html')
@login_required
def view_book(request):
    k=Book.objects.all() # same as select * from Books return all the data
    context={'book':k} #key value pair dictonary used to show values from views to html
    return render(request,'view_book.html',context)

def details(request,p):
    b=Book.objects.get(id=p)
    context={'book':b}
    return render(request,'details.html',context)

def edit(request,p):
    b=Book.objects.get(id=p)
    if(request.method=="POST"): #check if form is submitted

        b.title=request.POST["title"]
        b.author=request.POST['author']
        b.language=request.POST['language']
        b.pages=request.POST['pages']
        b.price=request.POST['price']
        if(request.FILES.get('cover'))==None:
            b.save()
        else:
            b.cover=request.FILES.get('cover')
        if(request.FILES.get('pdf'))==None:
            b.save()
        else:
            b.pdf=request.FILES.get('pdf')
        b.save()
        return redirect('Books:view_book')

    context={'book':b}
    return render(request,'edit.html',context)

def delete(request,p):
    b=Book.objects.get(id=p)
    b.delete()
    return redirect('Books:view_book')

def searchbook(request):
    b=None
    query=''
    if request.method=='POST':
        query=request.POST['search']
        if query:
            b=Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))# Q is used to when logical operation are needed in django application only after Q |,and,or are used

    return render(request,'search.html',{"search":b,"query":query})