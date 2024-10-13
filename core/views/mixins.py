from django.db import transaction


class AtomicMixin:
    """A mixin that ensures requests are wrapped in a transaction."""
    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

