from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='Shop'
urlpatterns = [
    path('',views.categories,name='categories'),
    path('search',views.searchitem,name='search'),
    path('add_category',views.add_category,name='add_category'),
    path('add_product',views.add_product,name='add_product'),
    path('product/<str:pk>',views.product,name='product'),
    path('detail/<str:pk>',views.productdetail,name='detail'),
    path('add_stock/<str:pk>',views.add_stock,name='add_stock'),
    path('register',views.register,name='register'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)