
from market.celery import celery_app
from market.celery.base import logger


@celery_app.task(name='notification_payment')
def notification_payment(cart_id):
    print('ok shodedededededede')
    logger.error(f"Error processing task: ")

    return 'okkkkkkk'

