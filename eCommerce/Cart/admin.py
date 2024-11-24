from django.contrib import admin
from .models import Cart,OrderDetail,Payment
# Register your models here.
admin.site.register(Cart)
admin.site.register(OrderDetail)
admin.site.register(Payment)