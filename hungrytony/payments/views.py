from payments.models import Payment as ModelPayment
from restaurant.models import Settings

from yookassa import Configuration
from yookassa import Payment


def create_payment(order_id, table_id, cost, info):
    settings = Settings.objects.last()

    Configuration.account_id = settings.account_id
    Configuration.secret_key = settings.secret_key

    payment = Payment.create(
        {
            'amount': {
                'value': '{}.00'.format(cost),
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://goodgameclubs.ru/'
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
        cost=cost
    )
