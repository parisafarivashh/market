from django.core.cache import cache

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

