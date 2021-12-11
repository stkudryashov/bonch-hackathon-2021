from payments.models import Payment as ModelPayment
from payments.models import ShopSettings

from yookassa import Configuration
from yookassa import Payment


def create_payment(order_id, table_id, cost, info):
    shop_settings = ShopSettings.objects.last()

    Configuration.account_id = shop_settings.account_id
    Configuration.secret_key = shop_settings.secret_key

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
        order_id=club.id_name,
        table_id=user.user_id,
        payment_id=payment.id,
        status=payment.status,
        info=info,
        cost=cost
    )
