from .models import Product,Category

def links(request):
    c=Category.objects.all()
    return {"links":c}