from django.urls import path
from payments.views import *

urlpatterns = [
    path('', create_payment, name='payment'),
    path('<str:payment_id>/', payment_page, name='payment_url'),
]
