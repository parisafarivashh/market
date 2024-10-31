

def get_or_none(model, _id: int):
    try:
        instance = model.objects.get(id=_id)
        return instance
    except model.DoesNotExist():
        return None

