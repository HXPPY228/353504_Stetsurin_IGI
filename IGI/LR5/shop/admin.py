from django.contrib import admin
from django.utils.html import format_html
from .models import ProductType, Product, Client, Order, OrderItem, Article, CompanyInfo, GlossaryTerm, Contact, Vacancy, Review, PromoCode, Tag, Partner

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
    list_display = ('full_name', 'email', 'phone', 'assigned_to')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    list_filter  = ('assigned_to',)

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def email(self, obj):
        return obj.user.email

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = ('title','published_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter   = ('published_at',)
    search_fields = ('title','teaser','body')
    filter_horizontal = ('tags',)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('year','description')

@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ('term','added_at')
    list_filter  = ('added_at',)
    search_fields = ('term','definition')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','role','phone','email')
    search_fields = ('name','role')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display  = ('title','posted_at')
    list_filter   = ('posted_at',)
    search_fields = ('title','description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('__str__','rating','published_at')
    list_filter   = ('rating','published_at')
    search_fields = ('name','text','user__username')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display  = ('code','discount','active','created_at','expires_at')
    list_filter   = ('active','created_at')
    search_fields = ('code',)
    
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'order', 'logo_tag')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)
    ordering = ('order', 'name')

    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;">', obj.logo.url)
        return '—'
    logo_tag.short_description = 'Логотип'