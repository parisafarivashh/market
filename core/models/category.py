from django.db import models

from .mixins import BaseModelMixin


class CustomQueryset(models.QuerySet):

    def not_removed(self):
        return self.filter(removed_at__isnull=True)

    def removed(self):
        return self.filter(removed_at__isnull=False)


class CustomManager(models.Manager):

    def get_queryset(self):
        return CustomQueryset(self.model, self._db)

    def not_removed(self):
        return self.get_queryset().not_removed()

    def removed(self):
        return self.get_queryset().removed()


class Category(BaseModelMixin):
    title = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='childrens',
    )

    objects = CustomManager()

    class Meta:
        db_table = 'category'

