from django.contrib import admin
from .models import ProductType, Product, Client, Order, OrderItem

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display    = ('code','name','product_type','price','in_production')
    list_filter     = ('product_type','in_production')
    search_fields   = ('code','name')
    list_editable   = ('price','in_production')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id','client','created_at','total_price')
    inlines       = (OrderItemInline,)
    readonly_fields = ('total_price',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ('first_name','last_name','email','phone')
    search_fields = ('first_name','last_name','email')
