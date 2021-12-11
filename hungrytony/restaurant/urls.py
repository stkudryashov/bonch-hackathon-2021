from django.urls import path
from restaurant.views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('reserve/', reserve_table, name='reserve')
]
