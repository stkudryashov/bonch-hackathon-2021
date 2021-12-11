from django.urls import path
from restaurant.views import *

urlpatterns = [
    path('', select_table, name='index'),
]
