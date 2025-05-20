from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Product, ProductType, Order, Client, Article, CompanyInfo, GlossaryTerm, Contact, Vacancy, PromoCode, Review
from .forms import OrderForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.db.models import Sum
import requests

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
    
class SellerRequiredMixin(UserPassesTestMixin):
    """Доступно только пользователям со статусом staff"""
    def test_func(self):
        return self.request.user.is_staff
    
    login_url = reverse_lazy('login')
    
class SellerDashboardView(SellerRequiredMixin, TemplateView):
    template_name = 'shop/seller_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # клиенты, назначенные этому продавцу
        clients = user.clients_assigned.all()
        # заказы этих клиентов
        orders  = Order.objects.filter(client__in=clients).order_by('-created_at')

        ctx['clients'] = clients
        ctx['orders']  = orders
        ctx['total_sales'] = orders.aggregate(
            total=Sum('total_price')
        )['total'] or 0
        return ctx
    
class HomeView(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        # Последняя статья
        ctx['latest'] = Article.objects.order_by('-published_at').first()

        # 1) Breaking Bad Quote
        try:
            resp = requests.get('https://api.breakingbadquotes.xyz/v1/quotes')
            resp.raise_for_status()
            data = resp.json()
            # API возвращает список из одного объекта
            ctx['bb_quote'] = data[0]  
        except Exception:
            ctx['bb_quote'] = {'quote': 'Не удалось получить цитату.', 'author': ''}

        # 2) Случайный шутка из Official Joke API
        try:
            resp2 = requests.get('https://official-joke-api.appspot.com/jokes/random')
            resp2.raise_for_status()
            ctx['joke'] = resp2.json()
        except Exception:
            ctx['joke'] = {'setup': 'Не удалось получить шутку.', 'punchline': ''}

        return ctx

class AboutView(ListView):
    model = CompanyInfo
    template_name = 'shop/about.html'
    context_object_name = 'timeline'

class NewsListView(ListView):
    model = Article
    template_name = 'shop/news_list.html'
    context_object_name = 'articles'
    paginate_by = 10

class GlossaryListView(ListView):
    model = GlossaryTerm
    template_name = 'shop/glossary.html'
    context_object_name = 'terms'

class ContactListView(ListView):
    model = Contact
    template_name = 'shop/contacts.html'
    context_object_name = 'contacts'

class PrivacyView(TemplateView):
    template_name = 'shop/privacy.html'

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'shop/vacancies.html'
    context_object_name = 'vacancies'

class PromoListView(ListView):
    model = PromoCode
    template_name = 'shop/promocodes.html'
    context_object_name = 'promocodes'

class ReviewListView(ListView):
    model = Review
    template_name = 'shop/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'shop/review_form.html'
    success_url = reverse_lazy('shop:reviews')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = (
            self.request.user.get_full_name() or 
            self.request.user.username
        )
        return super().form_valid(form)