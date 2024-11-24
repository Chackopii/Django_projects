from .models import Cart
from django.db.models import Aggregate,Sum,F

def count(request):
    count=0
    total=0
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        cart = cart.annotate(total_price=F('quantity') * F('product__price'))
        total = cart.aggregate(total=Sum('total_price'))['total'] or 0
        for i in cart:
            count += i.quantity
    return {'count':count,
            'total':total}