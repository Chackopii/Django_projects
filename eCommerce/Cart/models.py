from django.db import models
from Shop.models import Product
from django.contrib.auth.models import User
# Create your models here.


class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    add_on=models.DateTimeField(auto_now_add=True)


    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    no_of_items = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    pin = models.CharField(max_length=10)

    order_id =  models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30,default="Pending")
    delivery_status = models.CharField(max_length=30,default="Pending")
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class Payment(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=30)
    razorpay_payment_id = models.CharField(max_length=30, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id
