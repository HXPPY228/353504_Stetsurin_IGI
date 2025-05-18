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
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id','client','created_at','total_price')
    readonly_fields = ('total_price',)
    inlines = [OrderItemInline]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def email(self, obj):
        return obj.user.email

