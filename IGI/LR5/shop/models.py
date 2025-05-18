from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

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
