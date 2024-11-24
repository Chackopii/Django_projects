from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=30) #
    author=models.CharField(max_length=50)
    Language=models.CharField(max_length=20)
    price=models.IntegerField() #number
    pages=models.IntegerField() #number
    cover=models.ImageField(upload_to='image') #image
    pdf=models.FileField(upload_to='pdf') #file