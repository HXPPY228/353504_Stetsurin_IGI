from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, View
from django import forms
from django.urls import reverse_lazy
from .models import Product, ProductType, Order, Client, Article, CompanyInfo, GlossaryTerm, Contact, Vacancy, PromoCode, Review, OrderItem, Partner,CompanyTimeline
from .forms import OrderForm, ReviewForm, SignUpForm, OrderItemFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, DecimalField, ExpressionWrapper, F, Q
import requests
from statistics import mean, median, multimode
from datetime import date
import datetime
from django.utils import timezone
import calendar
import pytz
import re
from django.contrib.auth import get_user_model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
import logging
from django.shortcuts import redirect, get_object_or_404, render

logger = logging.getLogger('shop')

class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset().select_related('product_type')

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(code__icontains=q) |
                Q(product_type__name__icontains=q)
            )

        sort = self.request.GET.get('sort', 'name')
        if sort in ('name', 'price', 'product_type'):
            if sort == 'product_type':
                qs = qs.order_by('product_type__name')
            else:
                qs = qs.order_by(sort)
        else:
            qs = qs.order_by('name')

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
            
            logger.info(
                "New order #%s created by user %s (client_id=%s)",
                self.object.id,
                self.request.user.username,
                client.id
            )
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
class OrderOwnerMixin(LoginRequiredMixin):
    """Ограничивает доступ к заказам только их владельцу (клиенту)."""
    def get_queryset(self):
        client = self.request.user.client_profile
        return super().get_queryset().filter(client=client)
    
class OrderUpdateView(OrderOwnerMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/order_update.html'
    success_url = reverse_lazy('shop:my_orders')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = OrderItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            # Пересчёт общей суммы
            total = sum(item.product.price * item.quantity for item in self.object.items.all())
            self.object.total_price = total
            self.object.save()
            
            logger.info(
                "Order #%s updated by user %s", 
                self.object.id, 
                self.request.user.username
            )
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
class OrderDeleteView(OrderOwnerMixin, DeleteView):
    model = Order
    template_name = 'shop/order_confirm_delete.html'
    success_url = reverse_lazy('shop:my_orders')

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
        return Order.objects.filter(
            client__user=self.request.user
        ).exclude(status='cart').order_by('-created_at')
    
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

        if self.request.user.is_authenticated:
        # 1) Breaking Bad Quote
            try:
                resp = requests.get('https://api.breakingbadquotes.xyz/v1/quotes')
                resp.raise_for_status()
                data = resp.json()
                ctx['bb_quote'] = data[0]  
            except Exception as e:
                logger.error("Error getting BB Quote: %s", e, exc_info=True)
                ctx['bb_quote'] = {'quote': 'Не удалось получить цитату.', 'author': ''}

            # 2) Случайный шутка
            try:
                resp2 = requests.get('https://official-joke-api.appspot.com/jokes/random')
                resp2.raise_for_status()
                ctx['joke'] = resp2.json()
            except Exception as e:
                logger.error("Error getting joke: %s", e, exc_info=True)
                ctx['joke'] = {'setup': 'Не удалось получить шутку.', 'punchline': ''}
        else:
            # Для анонимов — показываем приглашение войти
            ctx['bb_quote'] = None
            ctx['joke']    = None
            
        ctx['partners'] = Partner.objects.filter(is_active=True).order_by('order', 'name')
        return ctx

class AboutView(TemplateView):
    template_name = 'shop/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyInfo.objects.first() 
        context['timeline'] = CompanyTimeline.objects.all()
        return context

class NewsListView(ListView):
    model = Article
    template_name = 'shop/news_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
class NewsDetailView(DetailView):
    model = Article
    template_name = 'shop/news_detail.html'
    context_object_name = 'article'
    
class NewsByTagListView(ListView):
    model = Article
    template_name = 'shop/news_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs['slug']).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tag'] = self.kwargs['slug']
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        all_codes = PromoCode.objects.all().order_by('-expires_at')
        context['active_promocodes'] = [p for p in all_codes if p.is_active]
        context['expired_promocodes'] = [p for p in all_codes if not p.is_active]
        return context

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
    
def get_user_timezone(request):
    tzname = request.COOKIES.get('user_timezone')
    try:
        return pytz.timezone(tzname)
    except Exception:
        return timezone.get_default_timezone()
    
class TimeInfoView(TemplateView):
    template_name = 'shop/time_info.html'

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)

        # 1) Определяем тайм-зону из куки
        user_tz = get_user_timezone(self.request)
        ctx['tz_name'] = str(user_tz)

        # 2) Текущее время UTC и в user_tz
        now_utc = datetime.datetime.now(pytz.UTC)
        now_local = now_utc.astimezone(user_tz)
        ctx['now_utc']   = now_utc.strftime("%d/%m/%Y %H:%M:%S")
        ctx['now_local'] = now_local.strftime("%d/%m/%Y %H:%M:%S")

        # 3) Последняя статья
        art = Article.objects.order_by('-published_at').first()
        if art:
            utc = art.published_at.astimezone(pytz.UTC)
            loc = utc.astimezone(user_tz)
            ctx['article']       = art
            ctx['article_utc']   = utc.strftime("%d/%m/%Y %H:%M:%S")
            ctx['article_local'] = loc.strftime("%d/%m/%Y %H:%M:%S")

        # 4) Последний заказ
        ord = Order.objects.order_by('-created_at').first()
        if ord:
            utc = ord.created_at.astimezone(pytz.UTC)
            loc = utc.astimezone(user_tz)
            ctx['order']       = ord
            ctx['order_utc']   = utc.strftime("%d/%m/%Y %H:%M:%S")
            ctx['order_local'] = loc.strftime("%d/%m/%Y %H:%M:%S")

        # 5) Последний отзыв
        rev = Review.objects.order_by('-published_at').first()
        if rev:
            utc = rev.published_at.astimezone(pytz.UTC)
            loc = utc.astimezone(user_tz)
            ctx['review']       = rev
            ctx['review_utc']   = utc.strftime("%d/%m/%Y %H:%M:%S")
            ctx['review_local'] = loc.strftime("%d/%m/%Y %H:%M:%S")

        # 6) Текстовый календарь
        today = now_local.date()
        ctx['calendar_text'] = calendar.TextCalendar().formatmonth(today.year, today.month)

        return ctx

class SalesByTypeChartView(View):
    def get(self, request, *args, **kwargs):
        # Собираем данные
        qs = (
            OrderItem.objects
            .values(type_name=F('product__product_type__name'))
            .annotate(
                revenue=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('product__price'),
                        output_field=DecimalField()
                    )
                )
            )
            .order_by('type_name')
        )

        types = [row['type_name'] for row in qs]
        revenues = [float(row['revenue']) for row in qs]

        # Создаем фигуру с контекстным менеджером
        with plt.ioff():  # Отключаем интерактивный режим
            fig = plt.figure(figsize=(8,4))
            plt.bar(range(len(types)), revenues)
            plt.xticks(range(len(types)), types, rotation=45, ha='right')
            plt.ylabel('Выручка, ₽')
            plt.title('Выручка по типам товаров')
            plt.tight_layout()

            # Сохраняем в буфер
            buf = BytesIO()
            fig.savefig(buf, format='png')
            plt.close(fig)  # Явно закрываем фигуру

        buf.seek(0)
        return HttpResponse(buf.getvalue(), content_type='image/png')
    
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        client, _ = Client.objects.get_or_create(user=request.user)

        order = Order.objects.filter(client=client, status='cart').first()
        if not order:
            order = Order.objects.create(client=client, status='cart', total_price=0)

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()

        order.total_price = sum(i.product.price * i.quantity for i in order.items.all())
        order.save()

        return redirect('shop:cart_detail')


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/cart_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = self.request.user.client_profile
        order = Order.objects.filter(client=client, status='cart').first()
        ctx['order'] = order
        return ctx


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        action = request.POST.get('action')
        item = get_object_or_404(
            OrderItem,
            pk=item_id,
            order__client=request.user.client_profile,
            order__status='cart'
        )

        if action == 'inc':
            item.quantity += 1
            item.save()
        elif action == 'dec':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        elif action == 'del':
            item.delete()

        if item.order:
            item.order.recalc_total()

        return redirect('shop:cart_detail')


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'shop/checkout.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, client__user=request.user, status='cart')
        return render(request, self.template_name, {'order': order})

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, client__user=request.user, status='cart')
        payment_method = request.POST.get('payment_method')

        if payment_method == 'cod':
            order.status = 'placed'
            order.save()
            return redirect('shop:my_orders')

        elif payment_method == 'online':
            card_number = request.POST.get('card_number', '').replace(' ', '')
            exp_date = request.POST.get('exp_date', '')
            cvv = request.POST.get('cvv', '')

            # Валидация карты
            errors = []
            if not re.fullmatch(r'\d{16}', card_number):
                errors.append('Номер карты должен состоять из 16 цифр.')
            if not re.fullmatch(r'(0[1-9]|1[0-2])\/\d{2}', exp_date):
                errors.append('Срок действия должен быть в формате MM/YY, месяц 01-12.')
            if not re.fullmatch(r'\d{3}', cvv):
                errors.append('CVV должен состоять из 3 цифр.')

            if errors:
                return render(request, self.template_name, {
                    'order': order,
                    'error': ' '.join(errors)
                })

            # Если всё ок — имитируем успешную оплату
            order.status = 'paid'
            order.save()
            return redirect('shop:my_orders')

        return render(request, self.template_name, {
            'order': order,
            'error': 'Выберите способ оплаты!'
        })