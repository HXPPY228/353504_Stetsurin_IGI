from django.urls import re_path
from . import views

app_name = 'shop'

urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^products/$', views.ProductListView.as_view(), name='product_list'),
    re_path(r'^products/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^order/new/$', views.OrderCreateView.as_view(), name='order_create'),
    re_path(r'^orders/$', views.MyOrdersView.as_view(), name='my_orders'),
    re_path(r'^dashboard/$', views.SellerDashboardView.as_view(), name='seller_dashboard'),
    re_path(r'^about/$', views.AboutView.as_view(), name='about'),
    re_path(r'^news/$', views.NewsListView.as_view(), name='news_list'),
    re_path(r'^glossary/$', views.GlossaryListView.as_view(), name='glossary'),
    re_path(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),
    re_path(r'^privacy/$', views.PrivacyView.as_view(), name='privacy'),
    re_path(r'^vacancies/$', views.VacancyListView.as_view(), name='vacancies'),
    re_path(r'^promocodes/$', views.PromoListView.as_view(), name='promocodes'),
    re_path(r'^reviews/$', views.ReviewListView.as_view(), name='reviews'),
    re_path(r'^reviews/new/$', views.ReviewCreateView.as_view(), name='review_create'),
]
