import json
import logging
import traceback
from celery import Task
from market.utility import get_or_none


logger = logging.getLogger('celery')


class MarketCelery(Task):
    autoretry_for = (Exception,)
    default_retry_delay = 2
    soft_time_limit = None
    needs_token = False
    max_retries = 100
    time_limit = None
    acks_late = True

    def __call__(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user_id = kwargs.get('user_id')
        self.user = None

        if user_id:
            self.user = get_or_none(User, user_id)

        return super().__call__(*args, **kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        if self.retry == 0:
            error_detail = json.dumps(dict(
                exc=exc.__doc__,
                task_id=task_id,
                stackTrace=traceback.format_exc(),
            ))
            logger.error(error_detail)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        error_detail = json.dumps(dict(
            exc=exc.__doc__,
            task_id=task_id,
            stackTrace=traceback.format_exc(),
        ))
        logger.error(error_detail)

