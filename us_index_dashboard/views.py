from django.shortcuts import render
from django.views.generic import ListView
from .models import DjiTest,IxicTest,NdxTest



def home(request):
  return render(request, "us_index_dashboard/home.html")


# Create your views here.
class DjiView(ListView):
    model = DjiTest
    template_name = 'us_index_dashboard/dji_chart.html'



class IxicView(ListView):
    model = IxicTest
    template_name = 'us_index_dashboard/ixic_chart.html'


class NdxView(ListView):
    model = NdxTest
    template_name = 'us_index_dashboard/ndx_chart.html'

##以下为测试
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from .models import Purchase, Item
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


def get_filter_options(request):
    grouped_purchases = Purchase.objects.annotate(year=ExtractYear('time')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })

#以下为dji画图函数
def get_dji_chart_price(request):
    time = DjiTest.objects.values_list('time',flat=True)
    close = DjiTest.objects.values_list('close',flat=True)
    return JsonResponse({
        'title': 'DJI Close Price',
        'data': {
            'labels': list(time),
            'datasets': [{
                'label': 'close price',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(close),
                'fill': False,
                'borderWidth': 1,
                'pointRadius': 0,
            }]
        },
    })

def get_dji_chart_2(request):
    time = DjiTest.objects.values_list('time',flat=True)
    bsadf_mi = DjiTest.objects.values_list('bsadf_mi',flat=True)
    rho_45 = DjiTest.objects.values_list('rho_45',flat=True)
    return JsonResponse({
        'title': 'DJI 2',
        'data': {
            'labels': list(time),

            'datasets': [{
                'label': ['bsadf_mi'],
                'backgroundColor': '#81ecec',
                'borderColor': '#81ecec',
                'data': list(bsadf_mi),
                'fill': False,
                'borderWidth': 1,
                'pointRadius': 0,
            },
            {
                'label': ['rho_45'],
                'backgroundColor': '#fab1a0',
                'borderColor': '#fab1a0',
                'data': list(rho_45),
                'fill': False,
                'borderWidth': 1,
                'pointRadius': 0,
            }]
        },
    })



def spend_per_customer_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)
    grouped_purchases = purchases.annotate(price=F('item__price')).annotate(month=ExtractMonth('time'))\
        .values('month').annotate(average=Avg('item__price')).values('month', 'average').order_by('month')

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Spend per customer in {year}',
        'data': {
            'labels': list(spend_per_customer_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(spend_per_customer_dict.values()),
            }]
        },
    })



def payment_success_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)

    return JsonResponse({
        'title': f'Payment success rate in {year}',
        'data': {
            'labels': ['Successful', 'Unsuccessful'],
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': [
                    purchases.filter(successful=True).count(),
                    purchases.filter(successful=False).count(),
                ],
            }]
        },
    })



def payment_method_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)
    grouped_purchases = purchases.values('payment_method').annotate(count=Count('id'))\
        .values('payment_method', 'count').order_by('payment_method')

    payment_method_dict = dict()

    for payment_method in Purchase.PAYMENT_METHODS:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        payment_method_dict[dict(Purchase.PAYMENT_METHODS)[group['payment_method']]] = group['count']

    return JsonResponse({
        'title': f'Payment method rate in {year}',
        'data': {
            'labels': list(payment_method_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': generate_color_palette(len(payment_method_dict)),
                'borderColor': generate_color_palette(len(payment_method_dict)),
                'data': list(payment_method_dict.values()),
            }]
        },
    })

##测试结束

##view测试
def statistics_view(request):
    return render(request, 'us_index_dashboard/statistics.html', {})
##view测试结束


def dji_chart_view(request):
    return render(request, 'us_index_dashboard/dji_chart.html', {})


