from django.urls import path
from payments.views import *

urlpatterns = [
    path('', create_payment, name='payment'),
]
