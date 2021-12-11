from django.shortcuts import render, redirect
from django.db.models import Sum
from orders.models import *


def index_view(request, secret_uuid):
    products = ProductCategory.objects.all()
    order = Order.objects.get(order_id=secret_uuid)

    order_cost = order.products.all().aggregate(sum=Sum('cost')).get('sum')

    if order_cost is None:
        order_cost = 0

    args = {
        'categories': products,
        'secret_uuid': secret_uuid,
        'order_cost': order_cost
    }

    return render(request, 'orders/content.html', args)


def add_product_to_order(request, secret_uuid):
    if not request.method == 'POST':
        return

    order = Order.objects.get(order_id=secret_uuid)
    product = request.POST.get('product_id')

    order.products.add(product)

    return redirect(f'/order/{secret_uuid}/')
