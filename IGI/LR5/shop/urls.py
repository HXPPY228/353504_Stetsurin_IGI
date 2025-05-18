from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('order/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/', views.MyOrdersView.as_view(), name='my_orders'),
]
