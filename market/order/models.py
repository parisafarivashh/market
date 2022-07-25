from django.db import models

from user.models import User
from product.models import Detail


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)

    @property
    def final_cost(self):
        cost = 0
        for item in self.items.all():
            cost += item.cost
        return cost


class ItemOrder(models.Model):
    price = models.FloatField()
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    count = models.IntegerField()

    class Meta:
        db_table = 'ItemOrder'

    @property
    def cost(self):
        return self.price * self.count

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        super(ItemOrder, self).delete(*args, **kwargs)
        self.detail.count += self.count
        self.detail.save()

