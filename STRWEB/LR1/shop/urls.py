from django.urls import re_path
from . import views

app_name = 'shop'

urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^products/$', views.ProductListView.as_view(), name='product_list'),
    re_path(r'^products/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^order/new/$', views.OrderCreateView.as_view(), name='order_create'),
    re_path(r'^order/(?P<pk>\d+)/edit/$', views.OrderUpdateView.as_view(), name='order_update'),
    re_path(r'^order/(?P<pk>\d+)/delete/$', views.OrderDeleteView.as_view(), name='order_delete'),
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
    re_path(r'^stats/$', views.StatsView.as_view(), name='stats'),
    re_path(r'^stats/chart/$', views.SalesByTypeChartView.as_view(), name='stats_chart'),
    re_path(r'^time/$', views.TimeInfoView.as_view(), name='time_info'),
    
    re_path(r'^cart/$', views.CartDetailView.as_view(), name='cart_detail'),
    re_path(r'^cart/add/(?P<pk>\d+)/$', views.AddToCartView.as_view(), name='add_to_cart'),
    re_path(r'^cart/item/(?P<pk>\d+)/update/$', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    re_path(r'^cart/checkout/$', views.CheckoutView.as_view(), name='checkout'),
    re_path(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    re_path(r'^news/(?P<slug>[-\w]+)/$', views.NewsDetailView.as_view(), name='news_detail'),
    re_path(r'^news/tag/(?P<slug>[-\w]+)/$', views.NewsByTagListView.as_view(), name='news_by_tag'),

]
