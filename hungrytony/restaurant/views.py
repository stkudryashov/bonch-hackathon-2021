from django.shortcuts import render
from restaurant.models import *


def index_view(request):
    tables = Table.objects.all()

    args = {
        'tables': tables
    }

    return render(request, 'restaurant/content.html', args)
