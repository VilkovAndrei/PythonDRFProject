import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY
NULLABLE = {'blank': True, 'null': True}


def convert_rub_to_usd(amount):
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)


def create_stripe_product(instance):

    title_product = f'{instance.course}' if instance.course else f'{instance.lesson}'
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get('id')


def create_stripe_price(summ, stripe_product_id):
    return stripe.Price.create(
        currency="usd",
        unit_amount=summ * 100,
        product=stripe_product_id
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url'), session.get('payment_status')

