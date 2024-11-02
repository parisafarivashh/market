from fileinput import close


def get_or_none(model, _id: int):
    try:
        instance = model.objects.get(id=_id)
        return instance
    except model.DoesNotExist():
        return None


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

