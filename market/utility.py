from functools import wraps

import ujson
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from rest_framework.response import Response

from market import settings


def get_or_none(model, _id: int):
    try:
        instance = model.objects.get(id=_id)
        return instance
    except model.DoesNotExist():
        return None

def delete_cache(key_prefix: str):
    """
    Delete all cache keys with the given prefix.
    """
    keys_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


#class Singleton:
#    _instance = None
#
#    def __new__(cls, *args, **kwargs):
#        if not cls._instance:
#            cls._instance = super().__new__(*args, **kwargs)
#
#        return cls._instance


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


def send_response_to_websocket(response, request):
        if not isinstance(response, Response):
            return

        channel_layer = get_channel_layer()
        path = request.path.replace('/api/', '')
        path = f"{request.method.lower()}_{path}".replace('/', '_')
        async_to_sync(channel_layer.group_send)(
            f"user__{request.user.id}",
            {
                "type": "send_data",
                "data": ujson.dumps({path: response.data}),
            },
        )


def login_required(resolver_func):

    @wraps(resolver_func)
    def wrapper_func(self, info, *args, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication credentials were not provided.")
        return resolver_func(self, info, *args, **kwargs)
    return wrapper_func

