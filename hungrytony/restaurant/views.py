from django.shortcuts import render
from restaurant.models import *


def select_table(request):
    tables = Table.objects.all()

    args = {
        'tables': tables
    }

    return render(request, 'restaurant/tables.html', args)
