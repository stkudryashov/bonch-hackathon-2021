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
        'order_cost': round(order_cost, 2)
    }

    return render(request, 'orders/content.html', args)


def add_product_to_order(request, secret_uuid):
    if not request.method == 'POST':
        return

    order = Order.objects.get(order_id=secret_uuid)
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)


    product_order = ProductOrder()
    product_order.order = order
    product_order.product = product
    product_order.save()

    return redirect(f'/order/{secret_uuid}/')
