from django.shortcuts import render, redirect

from restaurant.models import *
from orders.models import Order

import uuid


def index_view(request):
    tables = Table.objects.all()

    args = {
        'tables': tables
    }

    return render(request, 'restaurant/content.html', args)


def reserve_table(request):
    if not request.method == 'POST':
        return

    table_id = request.POST.get('table_id')
    table = Table.objects.get(id=table_id)

    table.is_free = False

    secret_uuid = uuid.uuid4()

    table.url = secret_uuid
    table.save()

    Order.objects.create(table_id=table, order_id=secret_uuid)

    return redirect(f'/order/{secret_uuid}/')
