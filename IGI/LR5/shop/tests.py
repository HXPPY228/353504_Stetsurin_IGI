from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.forms import SignUpForm, ReviewForm
from .models import Product, ProductType, Order, OrderItem, Client as ClientProfile, Article, CompanyInfo, GlossaryTerm, Contact, Vacancy, PromoCode, Review, Client
from datetime import date, timedelta
from .views import PromoListView

User = get_user_model()

class ShopTestCase(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass')
        self.seller.is_staff = True
        self.seller.save()
        self.user = User.objects.create_user(username='testuser', password='pass')

        self.client_profile = Client.objects.create(user=self.user, phone='+375 (29) 123-45-67', birth_date=date(2000,1,1), assigned_to=self.seller)

        self.pt = ProductType.objects.create(name='Торты')
        self.prod = Product.objects.create(code='T001', name='Торт', product_type=self.pt, price=100, in_production=True)

        self.client = TestClient()

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Торт')

    def test_order_crud(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('shop:order_create'), {
            'items-TOTAL_FORMS': '1',
            'items-INITIAL_FORMS': '0',
            'items-MIN_NUM_FORMS': '0',
            'items-MAX_NUM_FORMS': '1000',
            'items-0-product': str(self.prod.pk),
            'items-0-quantity': '2',
        })
        # redirect to product_list
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(client=self.client_profile)
        self.assertEqual(order.total_price, 200)
        # edit order
        response = self.client.post(reverse('shop:order_update', args=[order.pk]), {
            'items-TOTAL_FORMS': '1',
            'items-INITIAL_FORMS': '1',
            'items-MIN_NUM_FORMS': '0',
            'items-MAX_NUM_FORMS': '1000',
            'items-0-id': str(order.items.first().pk),
            'items-0-product': str(self.prod.pk),
            'items-0-quantity': '3',
        })
        self.assertRedirects(response, reverse('shop:my_orders'))
        order.refresh_from_db()
        self.assertEqual(order.total_price, 300)
        # delete order
        response = self.client.post(reverse('shop:order_delete', args=[order.pk]))
        self.assertRedirects(response, reverse('shop:my_orders'))
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())

    def test_review_create(self):
        # anonymous cannot
        response = self.client.get(reverse('shop:review_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('shop:review_create')}" )
        # login and create
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('shop:review_create'), {
            'rating': '5',
            'text': 'Great!',
        })
        self.assertRedirects(response, reverse('shop:reviews'))
        rev = Review.objects.get(user=self.user)
        self.assertEqual(rev.rating, 5)
        self.assertEqual(rev.text, 'Great!')

    def test_stats_view_staff(self):
        # создаём пользователя и делаем его staff
        user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)
        self.client.login(username='staffuser', password='12345')

        # доступ должен быть разрешён (200 OK)
        response = self.client.get(reverse('shop:stats'))
        self.assertEqual(response.status_code, 200)
        # staff
        self.client.login(username='seller', password='pass')
        response = self.client.get(reverse('shop:stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Клиенты')

    def test_signup_creates_client(self):
        new_client = TestClient()
        response = new_client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'complexP@ss1',
            'password2': 'complexP@ss1',
            'phone': '+375 (29) 987-65-43',
            'birth_date': '1990-05-20'
        })
        # redirect to login
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newuser')
        # client created
        self.assertTrue(Client.objects.filter(user=user).exists())

    def test_search_and_sort_products(self):
        # create extra product
        p2 = Product.objects.create(code='T002', name='Пирожное', product_type=self.pt, price=50)
        response = self.client.get(reverse('shop:product_list') + '?q=Пирожно&sort=price')
        self.assertEqual(response.status_code, 200)
        # ensure filtered and sorted
        products = response.context['products']
        self.assertEqual(list(products), [p2])

class FormsAndFiltersTestCase(TestCase):

    def test_signup_form_valid(self):
        eighteen_years_ago = date.today() - timedelta(days=18*365 + 5)
        form = SignUpForm(data={'username': 'newuser','first_name': 'Ivan','last_name': 'Ivanov','email': 'ivan@example.com','phone': '+375 (29) 123-45-67','birth_date': eighteen_years_ago.strftime('%Y-%m-%d'),'password1': 'complexpassword123','password2': 'complexpassword123',})
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_invalid_phone(self):
        bd = date.today() - timedelta(days=20*365)
        form = SignUpForm(data={
            'username': 'u',
            'first_name': '',
            'last_name': '',
            'email': 'e@e.com',
            'phone': '123456',
            'birth_date': bd.strftime('%Y-%m-%d'),
            'password1': 'pass1234',
            'password2': 'pass1234',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('Телефон в формате', form.errors['phone'][0])

    def test_signup_form_invalid_birth_date(self):
        seventeen_years_ago = date.today() - timedelta(days=17*365)
        form = SignUpForm(data={
            'username': 'younguser',
            'first_name': 'Юный',
            'last_name': 'Пользователь',
            'email': 'y@example.com',
            'phone': '+375 (29) 987-65-43',
            'birth_date': seventeen_years_ago.strftime('%Y-%m-%d'),
            'password1': 'abcd1234',
            'password2': 'abcd1234',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
        self.assertIn('не менее 18 лет', form.errors['birth_date'][0])

    def test_review_form_valid_and_invalid(self):
        form = ReviewForm(data={'rating': 4, 'text': 'Хорошо!'})
        self.assertTrue(form.is_valid(), form.errors)

        form = ReviewForm(data={'rating': 10, 'text': 'Супер!'})
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        form = ReviewForm(data={'rating': 3, 'text': '    '})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)