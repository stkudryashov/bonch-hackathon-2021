from django.urls import path
from orders.views import *

urlpatterns = [
    path('<uuid:secret_uuid>/', index_view, name='index'),
    path('add/<uuid:secret_uuid>/', add_product_to_order, name='add_product'),
]
