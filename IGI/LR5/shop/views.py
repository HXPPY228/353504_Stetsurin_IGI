from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import Product, ProductType, Order, Client, Article, CompanyInfo, GlossaryTerm, Contact, Vacancy, PromoCode, Review, OrderItem
from .forms import OrderForm, ReviewForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, DecimalField, ExpressionWrapper, F
import requests
from statistics import mean, median, multimode
from datetime import date
from django.utils import timezone
import calendar
import pytz
from django.contrib.auth import get_user_model

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
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Сначала создаём User
        response = super().form_valid(form)
        # Затем создаём профиль Client
        User = get_user_model()
        seller_user = User.objects.get(username='seller')
        
        Client.objects.create(
            user=self.object,               # только что сохранённый User
            phone=form.cleaned_data['phone'],
            birth_date=form.cleaned_data['birth_date'],
            assigned_to=seller_user
        )
        return response
    
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
        ctx['latest'] = Article.objects.order_by('-published_at').first()

        # 1) Breaking Bad Quote
        try:
            resp = requests.get('https://api.breakingbadquotes.xyz/v1/quotes')
            resp.raise_for_status()
            data = resp.json()
            ctx['bb_quote'] = data[0]  
        except Exception:
            ctx['bb_quote'] = {'quote': 'Не удалось получить цитату.', 'author': ''}

        # 2) Случайный шутка
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
    
class StatsView(LoginRequiredMixin, SellerRequiredMixin, TemplateView):
    template_name = 'shop/stats.html'

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)

        # 1) Список клиентов и товаров в алфавите
        ctx['clients_list'] = Client.objects.order_by('user__username')
        ctx['products_list'] = Product.objects.order_by('name')

        # Общая сумма продаж
        total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
        ctx['total_sales'] = total_sales

        # 2) Статистика по сумме продаж (для каждого заказа)
        sales = list(Order.objects.values_list('total_price', flat=True))
        ctx['sales_mean']   = mean(sales) if sales else 0
        ctx['sales_median'] = median(sales) if sales else 0
        # multimode возвращает список мод; возьмём самую маленькую
        modes = multimode(sales) if sales else []
        ctx['sales_mode']   = modes[0] if modes else None

        # 3) Статистика по возрасту клиентов
        ages = []
        for client in Client.objects.exclude(birth_date__isnull=True):
            # рассчитываем возраст
            bd = client.birth_date
            today = date.today()
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            ages.append(age)
        ctx['ages_mean']   = mean(ages) if ages else None
        ctx['ages_median'] = median(ages) if ages else None

        # 4) Какой тип товаров наиболее популярен? (по количеству позиций в заказах)
        pop = (Order.objects
               .values('items__product__product_type__name')
               .annotate(cnt=Count('items'))
               .order_by('-cnt')
               .first())
        ctx['most_popular_type'] = pop['items__product__product_type__name'] if pop else None
        ctx['most_popular_count'] = pop['cnt'] if pop else 0

        # 5) Какой тип товаров приносит наибольшую прибыль?
        profit_qs = (
            OrderItem.objects
            .values(type_name=F('product__product_type__name'))
            .annotate(
                total_profit=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('product__price'),
                        output_field=DecimalField(max_digits=12, decimal_places=2)
                    )
                )
            )
            .order_by('-total_profit')
        )

        if profit_qs:
            best = profit_qs[0]
            ctx['best_profit_type'] = best['type_name']
            ctx['best_profit_sum']  = best['total_profit']
        else:
            ctx['best_profit_type'] = None
            ctx['best_profit_sum']  = 0

        return ctx
    
class TimeInfoView(TemplateView):
    template_name = 'shop/time_info.html'

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)

        # 1) Задаём зону +3 вручную
        user_tz = pytz.timezone('Europe/Minsk')
        ctx['tz_name'] = user_tz.zone

        # 2) Текущее время в UTC и в user_tz
        now_utc   = timezone.now()
        now_local = now_utc.astimezone(user_tz)
        ctx['now_utc']   = now_utc.strftime("%d/%m/%Y %H:%M:%S")
        ctx['now_local'] = now_local.strftime("%d/%m/%Y %H:%M:%S")

        # 3) Последняя статья
        latest_article = Article.objects.order_by('-published_at').first()
        if latest_article:
            art_utc   = latest_article.published_at
            art_local = art_utc.astimezone(user_tz)
            ctx['article']       = latest_article
            ctx['article_utc']   = art_utc.strftime("%d/%m/%Y %H:%M:%S")
            ctx['article_local'] = art_local.strftime("%d/%m/%Y %H:%M:%S")

        # 4) Последний заказ
        latest_order = Order.objects.order_by('-created_at').first()
        if latest_order:
            ord_utc   = latest_order.created_at
            ord_local = ord_utc.astimezone(user_tz)
            ctx['order']       = latest_order
            ctx['order_utc']   = ord_utc.strftime("%d/%m/%Y %H:%M:%S")
            ctx['order_local'] = ord_local.strftime("%d/%m/%Y %H:%M:%S")

        # 5) Последний отзыв
        latest_review = Review.objects.order_by('-published_at').first()
        if latest_review:
            rev_utc   = latest_review.published_at
            rev_local = rev_utc.astimezone(user_tz)
            ctx['review']       = latest_review
            ctx['review_utc']   = rev_utc.strftime("%d/%m/%Y %H:%M:%S")
            ctx['review_local'] = rev_local.strftime("%d/%m/%Y %H:%M:%S")

        # 6) Текстовый календарь текущего месяца
        today = now_local.date()
        cal = calendar.TextCalendar()
        ctx['calendar_text'] = cal.formatmonth(today.year, today.month)

        return ctx