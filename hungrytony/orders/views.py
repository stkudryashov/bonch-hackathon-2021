from django.shortcuts import render
from orders.models import *


def index_view(request):
    products = ProductCategory.objects.all()

    args = {
        'categories': products
    }

    return render(request, 'orders/content.html', args)
