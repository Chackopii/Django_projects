import razorpay
from django.shortcuts import render,redirect
from .models import Cart,Payment,OrderDetail,User
from Shop.models import Product
from django.db.models import Aggregate,Sum,F
from django.contrib import messages

# Create your views here.
def add_to_cart(request,pk):
    product=Product.objects.get(id=pk)
    user= request.user
    if product.stock < 0:
        messages.error(request,"The product is out of stock")
        return redirect("Cart:cart_view")
    try:
        cart_item=Cart.objects.get(product=product,user=user)
        cart_item.quantity +=1
        cart_item.save()

    except:
        cart_item = Cart.objects.create(product=product, user=user, quantity=1)
        product.stock -= 1
        product.save()
        cart_item.save()

    return redirect("Cart:cart_view")

def cart_view(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    cart = cart.annotate(total_price=F('quantity') * F('product__price'))
    total=cart.aggregate(total=Sum('total_price'))['total'] or 0
    context={
        "cart":cart,
        "total":total
    }
    return render(request,"cart_view.html",context)

def delete_cart_item(request,pk):
    user=request.user
    product=Product.objects.get(id=pk)
    cart=Cart.objects.get(user=user,product=product)
    try:
        if cart.quantity > 1: #checking if quantity is greater than 0
            cart.quantity -=1
            product.stock +=1
            product.save()
            cart.save()
        else: # if quantity becomes 0
            cart.delete() #delete cart product
            product.stock +=1 #adding last 1 stock when cart is deleted
            product.save() # saving the changes
    except:
        pass
    return redirect("Cart:cart_view")

def delete_cart(request):
    user = request.user
    product = Product.objects.get(id=pk)
    try:
        cart = Cart.objects.get(user=user, product=product)
        cart.delete()
        cart.save()
    except:
        pass
    return redirect("Cart:cart_view")

def orderform(request):
    if request.method == 'POST':
        address=request.POST['address']
        phone = request.POST['phone']
        pin = request.POST['pin']

        total=0
        user = request.user
        cart = Cart.objects.filter(user=user).select_related('product')
        total = sum(item.product.price * item.quantity for item in cart)
        print(total)

        #razorpay conenction
        client=razorpay.Client(auth=('rzp_test_4dDYIqQwrl8aCV','T92lz9vhN9VcQuK32XECjC4b'))

        #razorpay order creation
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        order_id=response_payment['id'] #return order id
        print(order_id)
        status = response_payment['status'] #return the status from response
        print(status)
        if status=="created":
            payments=Payment.objects.create(name=user.username,amount=total,order_id=order_id)
            payments.save()
            print(payments)

            for order in cart:
                orders=OrderDetail.objects.create(product=order.product,user=order.user,address=address,phone=phone,pin=pin,no_of_items=order.quantity,order_id=order_id)
                # o = orderdetails.objects.create(product=i.product, user=i.user, phone=pn, address=a, pincode=n,orderid=order_id)
                # o.save()
                orders.save()
            context={
                'payment':response_payment,
                'name':user.username
            }
            return render(request,'payment.html',context)
    return render(request,'orderform.html')



from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
@csrf_exempt
def payment_status(request,uname):
    user=User.objects.get(username=uname) #getting user info
    login(request,user)

    response=request.POST #respose after payment successful
    #check the validity of payment deatils from razorpay
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],
    }
    client=razorpay.Client(auth=('rzp_test_4dDYIqQwrl8aCV','T92lz9vhN9VcQuK32XECjC4b'))
    try:
        #function to check the payment is valid and verify the payment
        status=client.utility.verify_payment_signature(param_dict)
        payment=Payment.objects.get(order_id=response['razorpay_order_id'])

        payment.razorpay_payment_id=response['razorpay_payment_id']
        payment.paid=True
        payment.save()

        orders=OrderDetail.objects.filter(order_id=response['razorpay_order_id']).select_related('product')
        for order in orders:
            order.payment_status='completed'
            order.save()
        # delete cart after the payment is succesfull for that particular user
        cart=Cart.objects.filter(user=user)
        cart.delete()

    except:
        pass

    return render(request, "payment_status.html", context={"status": status})


def orderview(request):
    user=request.user
    order_detail = OrderDetail.objects.filter(payment_status='completed').select_related('user')
    print(order_detail)
    # order_total= OrderDetail.objects.filter(order_id=order_detail.order_id,payment_status='completed').select_related('user')
    context={
        'orders':order_detail
    }
    return render(request,'orderview.html',context)

