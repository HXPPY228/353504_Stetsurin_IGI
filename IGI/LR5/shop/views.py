from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Product, ProductType, Order, Client
from .forms import OrderForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ProductListView(ListView):
    model = Product
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        # если в базе ещё нет ни одного продукта — создаём набор образцов
        if not qs.exists():
            samples = {
                'Кексы': [
                    ('CK001', 'Ванильный кекс', 60),
                    ('CK002', 'Шоколадный кекс', 70),
                    ('CK003', 'Клубничный кекс', 65),
                ],
                'Пирожные': [
                    ('PA001', 'Эклер со сливками', 80),
                    ('PA002', 'Профитроли', 75),
                    ('PA003', 'Картошка (пирожное)', 50),
                ],
                'Торты': [
                    ('TC001', 'Торт «Наполеон»', 500),
                    ('TC002', 'Чизкейк', 450),
                    ('TC003', 'Фруктовый торт', 550),
                ],
                'Печенья': [
                    ('CKG001', 'Шоколадное печенье', 40),
                    ('CKG002', 'Овсяное печенье', 45),
                    ('CKG003', 'Ванильное печенье', 35),
                ],
                'Пироги': [
                    ('PIE001', 'Яблочный пирог', 120),
                    ('PIE002', 'Вишнёвый пирог', 130),
                ],
            }
            # создаём типы и продукты
            for type_name, items in samples.items():
                pt, _ = ProductType.objects.get_or_create(
                    name=type_name,
                    defaults={'description': f'Вкусные изделия категории «{type_name}»'}
                )
                for code, name, price in items:
                    Product.objects.create(
                        code=code,
                        name=name,
                        product_type=pt,
                        price=price,
                        in_production=True
                    )
            qs = super().get_queryset()
        return qs

class ProductDetailView(DetailView):
    model = Product

class OrderCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Order
    form_class = OrderForm
    template_name = 'shop/order_create.html'
    success_url = reverse_lazy('shop:product_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # inlineformset хранится в form.items
        data['items'] = self.get_form().items
        return data

    def form_valid(self, form):
        client, created = Client.objects.get_or_create(
            user=self.request.user
        )
        self.object = form.save(commit=False)
        self.object.client = client
        self.object.total_price = 0
        self.object.save()

        items = self.get_context_data()['items']
        if items.is_valid():
            items.instance = self.object
            items.save()
            # пересчёт суммы
            total = sum(i.product.price * i.quantity for i in self.object.items.all())
            self.object.total_price = total
            self.object.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/my_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client__user=self.request.user)