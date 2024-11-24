from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name="Cart"

urlpatterns = [
    path("cart_view/",views.cart_view,name="cart_view"),
    path("add_to_cart/<str:pk>",views.add_to_cart,name="add_cart"),
    path("delete_cart_item/<str:pk>",views.delete_cart_item,name="delete_cart_item"),
    path("delete_cart/<str:pk>",views.delete_cart,name="delete_cart"),
    path("order_form",views.orderform,name="orderform"),
    path("order-view",views.orderview,name="order-view"),
    path("payment_status<str:uname>",views.payment_status,name="status"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)