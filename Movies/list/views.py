from django.shortcuts import render,redirect
from .models import Film


# Create your views here.

def home(request):
    k=Film.objects.all()
    context={'film':k}
    return render(request,'category.html',context)

def add_movie(request):
    if(request.method=='POST'):
        title=request.POST['title']
        description=request.POST['des']
        language=request.POST['lang']
        year=request.POST['year']
        image=request.FILES.get('img')
        form=Film.objects.create(title=title,description=description,language=language,year=year,image=image)
        form.save()
        return redirect('home')

    return render(request,'add_movie.html')

def details(request,p):
    b=Film.objects.get(id=p)
    context={"film":b}
    return render(request,'details.html',context)

def update(request,p):
    b=Film.objects.get(id=p)
    if request.method=='POST':
        b.title=request.POST['title']
        b.description=request.POST['des']
        b.language=request.POST['lang']
        b.year=request.POST['year']
        if request.FILES.get('img')==None:
            b.save()
        else:
            b.image=request.FILES.get('img')
        b.save()
        return redirect('details')

    context={"film":b}
    return render(request,'update.html',context)

def delete(request,p):
    b=Film.objects.get(id=p)
    b.delete()
    return redirect('home')