from django.shortcuts import render, redirect
from restaurant.models import *


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
    table.save()

    return redirect('/order/')
