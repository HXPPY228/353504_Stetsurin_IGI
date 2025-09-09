from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from datetime import date
from django.utils import timezone

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
    STATUS_CHOICES = [
        ('cart', 'Корзина'),
        ('placed', 'Оформлен'),
        ('paid', 'Оплачен'),
    ]
    client      = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    created_at  = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')
    
    def recalc_total(self):
        total = sum(item.line_total() for item in self.items.all())
        self.total_price = total
        self.save()

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
    name = models.CharField(max_length=255, verbose_name="Название компании")
    description = models.TextField(verbose_name="Описание")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Логотип")
    video_url = models.TextField(blank=True, null=True, help_text="Ссылка или путь к видео (например, /media/video/promo.mp4)")
    inn = models.CharField(max_length=12, blank=True, null=True, verbose_name="ИНН")
    ogrn = models.CharField(max_length=13, blank=True, null=True, verbose_name="ОГРН")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Юридический адрес")
    certificate = models.TextField(blank=True, help_text="Текст сертификата")

    def __str__(self):
        return self.name


class CompanyTimeline(models.Model):
    year = models.PositiveIntegerField(verbose_name="Год")
    description = models.TextField(verbose_name="Событие")

    class Meta:
        ordering = ('-year',) 

    def __str__(self):
        return f"{self.year}"


class GlossaryTerm(models.Model):
    term         = models.CharField(max_length=100, unique=True)
    definition   = models.TextField()
    added_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

class Contact(models.Model):
    # «Контакты»
    name         = models.CharField(max_length=100)
    role         = models.CharField(max_length=100, blank=True)
    photo        = models.ImageField(upload_to='contacts/', blank=True, null=True)
    phone        = models.CharField(max_length=50, blank=True)
    email        = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
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
    code       = models.CharField(max_length=50, unique=True)
    discount   = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_active(self):
        from django.utils import timezone
        if self.expires_at:
            return self.expires_at >= timezone.now()
        return True

    def __str__(self):
        return f"{self.code} ({'active' if self.is_active else 'archived'})"
    
class Partner(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    logo = models.ImageField(upload_to="logos/")
    is_active = models.BooleanField('Показывать', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name