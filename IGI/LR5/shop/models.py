from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from datetime import date

class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    in_production = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Client(models.Model):
    user  = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='client_profile')
    phone = models.CharField(max_length=20, blank=True)
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clients_assigned'
    )
    
    birth_date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Order(models.Model):
    client      = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    created_at  = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} – {self.client}"

class OrderItem(models.Model):
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity= models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def line_total(self):
        return self.product.price * self.quantity

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
    
class Article(models.Model):
    # для Главной и Новости
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    published_at = models.DateTimeField(auto_now_add=True)
    teaser       = models.CharField(max_length=250, blank=True)  # одно предложение
    body         = models.TextField()
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
        verbose_name='Тэги'
    )
    image        = models.ImageField(upload_to='news_images/', blank=True)

    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    # раздел «О компании»
    year         = models.PositiveIntegerField()
    description  = models.TextField()

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return str(self.year)

class GlossaryTerm(models.Model):
    # «Словарь терминов и понятий»
    term         = models.CharField(max_length=100, unique=True)
    definition   = models.TextField()
    added_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

class Contact(models.Model):
    # «Контакты»
    name         = models.CharField(max_length=100)
    role         = models.CharField(max_length=100, blank=True)
    photo        = models.ImageField(upload_to='contacts/', blank=True)
    phone        = models.CharField(max_length=50, blank=True)
    email        = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    # «Вакансии»
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    posted_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    # «Отзывы»
    user         = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.SET_NULL, null=True, blank=True)
    name         = models.CharField(max_length=100)
    rating       = models.PositiveSmallIntegerField()
    text         = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or self.user.username} ({self.rating}/5)"


class PromoCode(models.Model):
    # «Промокоды и купоны»
    code         = models.CharField(max_length=50, unique=True)
    discount     = models.DecimalField(max_digits=5, decimal_places=2)
    active       = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    expires_at   = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "active" if self.active else "archived"
        return f"{self.code} ({status})"