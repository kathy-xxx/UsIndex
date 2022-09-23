from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),

    path('chart/dji/price', views.get_dji_chart_price, name='chart-dji-price'),
    path('chart/dji/2', views.get_dji_chart_2, name='chart-dji-2'),
    ##以下为测试
     path('chart/filter-options/', views.get_filter_options, name='chart-filter-options'),
    path('chart/spend-per-customer/<int:year>/', views.spend_per_customer_chart, name='chart-spend-per-customer'),
    path('chart/payment-success/<int:year>/', views.payment_success_chart, name='chart-payment-success'),
    path('chart/payment-method/<int:year>/', views.payment_method_chart, name='chart-payment-method'),
    ##测试结束
    ##view测试
    path('statistics/', views.statistics_view, name='shop-statistics'),
    path('dji/', views.dji_chart_view, name='dji_chart'),
    ##view测试结束

]

urlpatterns += staticfiles_urlpatterns()