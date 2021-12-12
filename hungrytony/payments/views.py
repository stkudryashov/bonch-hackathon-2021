from django.shortcuts import redirect, render

from orders.models import Order
from payments.models import Payment as ModelPayment
from restaurant.models import Settings

from yookassa import Configuration
from yookassa import Payment


def create_payment(request):
    if not request.method == 'POST':
        return

    order_id = request.POST.get('order_id')
    order = Order.objects.get(order_id=order_id)

    table_id = order.table_id

    cost = request.POST.get('cost').replace(',', '.')
    info = request.POST.get('info')

    settings = Settings.objects.last()

    Configuration.account_id = settings.account_id
    Configuration.secret_key = settings.secret_key

    payment = Payment.create(
        {
            'amount': {
                'value': '{}'.format(cost),
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'http://127.0.0.1:8000/'
            },
            'capture': True,
            'description': info
        }
    )

    message = 'Для начала надо оплатить 🙂\n'

    ModelPayment.objects.create(
        order_id=order_id,
        table_id=table_id,
        payment_id=payment.id,
        status=payment.status,
        info=info,
        cost=float(cost)
    )

    args = {
        'url': payment.confirmation.confirmation_url
    }

    return redirect(f'/payment/{payment.id}/')


def payment_page(request, payment_id):
    settings = Settings.objects.last()

    Configuration.account_id = settings.account_id
    Configuration.secret_key = settings.secret_key

    payment = Payment.find_one(payment_id)

    args = {
        'url': payment.confirmation.confirmation_url
    }

    return render(request, 'payments/content.html', args)
