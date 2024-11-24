from django.db import models

# Create your models here.
class Film(models.Model):
    title=models.CharField(max_length=30)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    image=models.ImageField(upload_to='image/')