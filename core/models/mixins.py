from django.db import models


class BaseModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

